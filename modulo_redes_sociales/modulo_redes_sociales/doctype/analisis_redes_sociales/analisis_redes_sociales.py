# Copyright (c) 2025, Grupo 7 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
from datetime import datetime
from typing import Dict, Any


class AnalisisRedesSociales(Document):
    def before_save(self):
        """Set tracking fields before saving"""
        if self.is_new():
            self.creado_por = frappe.session.user
            self.fecha_creacion = datetime.now()
        self.modificado_por = frappe.session.user
        self.ultima_actualizacion = datetime.now()
        
        # Initialize clustering display field for clustering analysis
        if self.tipo_analisis == "Clustering" and not self.resumen_clustering_display:
            if self.estado == "Pendiente":
                self.resumen_clustering_display = "⏳ Análisis de clustering pendiente de ejecución..."
            elif self.estado == "En Progreso":
                self.resumen_clustering_display = "🔄 Ejecutando análisis de clustering..."
            elif self.estado == "Error":
                self.resumen_clustering_display = "❌ Error en el análisis de clustering. Revisar logs de ejecución."

    @frappe.whitelist()
    def ejecutar_analisis_dev(self):
        """Ejecutar análisis de forma directa (desarrollo)"""
        try:
            self.estado = "En Progreso"
            self.log_ejecucion = f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Iniciando análisis directo..."
            self.save()
            
            if self.tipo_analisis == "Predicción de Seguidores":
                return self._ejecutar_prediccion_dev()
            elif self.tipo_analisis == "Clustering":
                return self._ejecutar_clustering_dev()
            else:
                raise Exception(f"Tipo de análisis no soportado: {self.tipo_analisis}")
                
        except Exception as e:
            self.estado = "Error"
            self.error_message = str(e)
            self.log_ejecucion += f"\n[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ❌ Error: {str(e)}"
            
            # Update display field for error state
            if self.tipo_analisis == "Clustering":
                self.resumen_clustering_display = f"❌ Error en análisis de clustering:\n\n{str(e)}\n\nRevisar configuración de API y conectividad."
            
            self.save()
            return {"success": False, "error": str(e)}

    def _ejecutar_prediccion_dev(self) -> Dict[str, Any]:
        """Ejecutar predicción de seguidores de forma directa"""
        config_doc = frappe.get_doc("API Configuration", self.api_configuration)
        
        params = {
            "fecha": str(self.fecha_analisis) if self.fecha_analisis else datetime.now().strftime('%Y-%m-%d')
        }
        
        # El endpoint correcto: /regression/predict/{username}?fecha=YYYY-MM-DD
        endpoint = f"regression/predict/{self.usuario_red_social}"
        self.log_ejecucion += f"\n[DEBUG] Predicción - endpoint: {endpoint}, params: {params}"
        self.log_ejecucion += f"\n[DEBUG] Config API Name: {config_doc.name}"
        
        try:
            result = config_doc.make_api_request(endpoint, method="GET", params=params)
            self.log_ejecucion += f"\n[DEBUG] Request exitoso, resultado: {result}"
            
            if result:
                self._procesar_resultados(result)
                self.estado = "Completado"
                self.log_ejecucion += f"\n[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ✅ Predicción completada"
                self.save()
                return {"success": True, "result": result}
            else:
                self.log_ejecucion += f"\n[ERROR] La API no devolvió resultados válidos"
                raise Exception("La API no devolvió resultados válidos")
                
        except Exception as e:
            error_msg = str(e)
            if len(error_msg) > 100:
                error_msg = error_msg[:100] + "... (truncado)"
            self.log_ejecucion += f"\n[DEBUG] Error en predicción: {error_msg}"
            raise Exception(f"Error en predicción: {error_msg}")

    def _ejecutar_clustering_dev(self) -> Dict[str, Any]:
        """Ejecutar clustering de publicaciones de forma directa"""
        config_doc = frappe.get_doc("API Configuration", self.api_configuration)
        
        # El endpoint correcto: /clustering/clusters/{username}
        endpoint = f"clustering/clusters/{self.usuario_red_social}"
        self.log_ejecucion += f"\n[DEBUG] Clustering - endpoint: {endpoint}"
        try:
            result = config_doc.make_api_request(endpoint, method="GET")
            
            if result:
                self._procesar_resultados(result)
                self.estado = "Completado"
                self.log_ejecucion += f"\n[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ✅ Clustering completado"
                self.save()
                return {"success": True, "result": result}
            else:
                self.resumen_clustering_display = "⚠️ La API no devolvió resultados válidos para el clustering."
                raise Exception("La API no devolvió resultados válidos")
                
        except Exception as e:
            error_msg = str(e)
            if len(error_msg) > 100:
                error_msg = error_msg[:100] + "... (truncado)"
            self.log_ejecucion += f"\n[DEBUG] Error en clustering: {error_msg}"
            raise Exception(f"Error en clustering: {error_msg}")

    def _procesar_resultados(self, result):
        """Procesar y almacenar los resultados del análisis"""
        try:
            # Store raw response
            self.datos_raw = json.dumps(result, indent=2, ensure_ascii=False)
            
            # Process based on analysis type
            if self.tipo_analisis == "Predicción de Seguidores":
                self.log_ejecucion += f"\n[DEBUG] Estructura de respuesta recibida: {list(result.keys()) if isinstance(result, dict) else type(result)}"
                self.log_ejecucion += f"\nResultado recibido: {json.dumps(result, indent=2, ensure_ascii=False)}"
                
                if 'prediction' in result:
                    prediction_value = result.get('prediction', 0)
                    self.prediccion_seguidores = int(prediction_value) if prediction_value else 0
                    self.resultado_prediccion = str(prediction_value)
                    self.log_ejecucion += f"\n[DEBUG] Predicción procesada: {prediction_value} seguidores"
                    
                if 'confidence' in result:
                    self.confidence_score = float(result.get('confidence', 0.0))
                    
                # Log additional prediction details
                if 'model_type' in result:
                    self.log_ejecucion += f"\n[DEBUG] Modelo utilizado: {result.get('model_type')}"
                if 'target_variable' in result:
                    self.log_ejecucion += f"\n[DEBUG] Variable objetivo: {result.get('target_variable')}"
                    
            elif self.tipo_analisis == "Clustering":
                # Process clustering results according to API documentation
                self.log_ejecucion += f"\n[DEBUG] Estructura de respuesta recibida: {list(result.keys()) if isinstance(result, dict) else type(result)}"
                
                if 'clusters' in result:
                    clustering_data = result.get('clusters', [])
                    self.log_ejecucion += f"\n[DEBUG] Clusters encontrados: {len(clustering_data)}"
                    
                    self.resultado_clustering = json.dumps(clustering_data, indent=2, ensure_ascii=False)
                    
                    # Extract basic cluster info from API response
                    total_clusters = result.get('total_clusters', len(clustering_data))
                    
                    # Debug cluster structure
                    if clustering_data and len(clustering_data) > 0:
                        primer_cluster = clustering_data[0]
                        self.log_ejecucion += f"\n[DEBUG] Estructura primer cluster: {list(primer_cluster.keys()) if isinstance(primer_cluster, dict) else type(primer_cluster)}"
                        
                        self.cluster_asignado = primer_cluster.get('cluster_id', 0)
                        self.cluster_nombre = primer_cluster.get('nombre', f'Cluster {self.cluster_asignado}')
                        
                        # Check for examples/posts in cluster
                        publicaciones = primer_cluster.get('publicaciones', [])
                        self.log_ejecucion += f"\n[DEBUG] Publicaciones en primer cluster: {len(publicaciones)}"
                    
                    # Generate detailed summary with enhanced statistics
                    summary = self._generate_enhanced_clustering_summary(result, clustering_data)
                    self.resumen_clusters = json.dumps(summary, indent=2, ensure_ascii=False)
                    
                    # Generate user-friendly display text
                    self.resumen_clustering_display = self._format_clustering_display(summary)
                    
                    self.log_ejecucion += f"\n[INFO] Clustering procesado: {summary['total_clusters']} clusters, {summary['total_posts']} posts, cluster asignado: {self.cluster_asignado}"
                    
                else:
                    # Fallback for unexpected structure
                    self.log_ejecucion += f"\n[DEBUG] No se encontró 'clusters' en respuesta. Keys disponibles: {list(result.keys()) if isinstance(result, dict) else 'No es dict'}"
                    self.resultado_clustering = json.dumps(result, indent=2, ensure_ascii=False)
                    summary = self._generate_fallback_summary(result)
                    self.resumen_clusters = json.dumps(summary, indent=2, ensure_ascii=False)
                    self.resumen_clustering_display = self._format_clustering_display(summary)
                    self.log_ejecucion += f"\n[WARNING] Estructura de clustering inesperada, usando fallback"
                    
            # Store processed data for dashboard
            processed = {
                "tipo": self.tipo_analisis,
                "usuario": self.usuario_red_social,
                "timestamp": datetime.now().isoformat(),
                "result": result
            }
            self.datos_procesados = json.dumps(processed, indent=2, ensure_ascii=False)
            
        except Exception as e:
            error_msg = str(e)[:200] + "..." if len(str(e)) > 200 else str(e)
            self.log_ejecucion += f"\n[ERROR] Error procesando resultados: {error_msg}"

    @frappe.whitelist()
    def refrescar_analisis(self):
        """Refresh the analysis with latest data"""
        if self.estado in ["Completado", "Fallido"]:
            self.ejecutar_analisis_dev()
        else:
            frappe.throw("No se puede refrescar un análisis que está actualmente en progreso")

    def _generate_enhanced_clustering_summary(self, api_result: Dict[str, Any], clusters_data: list) -> Dict[str, Any]:
        """Generate enhanced summary from API clustering response"""
        # Get basic counts from API response
        total_clusters = api_result.get('total_clusters', len(clusters_data))
        
        self.log_ejecucion += f"\n[DEBUG] Generando resumen: total_clusters={total_clusters}, len(clusters_data)={len(clusters_data)}"
        
        if not clusters_data:
            return {
                "total_clusters": total_clusters,
                "total_posts": 0,
                "avg_engagement_rate": 0.0,
                "total_likes": 0,
                "total_comments": 0,
                "total_views": 0,
                "cluster_sizes": [],
                "summary_text": f"{total_clusters} clusters encontrados sin ejemplos disponibles",
                #"modelo_usado": api_result.get('modelo_usado', 'N/A')
            }
        
        # Calculate statistics from cluster examples
        total_posts = 0
        all_examples = []
        cluster_sizes = []
        cluster_names = []
        
        for i, cluster in enumerate(clusters_data):
            self.log_ejecucion += f"\n[DEBUG] Procesando cluster {i}: {list(cluster.keys()) if isinstance(cluster, dict) else type(cluster)}"
            
            if isinstance(cluster, dict):
                # Get cluster name - usando cluster ID si no hay nombre
                cluster_id = cluster.get('cluster', i)
                cluster_name = cluster.get('nombre', f"Cluster {cluster_id}")
                cluster_names.append(cluster_name)
                
                # Get publicaciones from cluster (not ejemplos)
                publicaciones = cluster.get('publicaciones', [])
                self.log_ejecucion += f"\n[DEBUG] Cluster {i} ({cluster_name}): {len(publicaciones)} publicaciones"
                
                cluster_sizes.append(len(publicaciones))
                total_posts += len(publicaciones)
                all_examples.extend(publicaciones)
            else:
                cluster_names.append(f"Cluster {i}")
                cluster_sizes.append(0)
        
        self.log_ejecucion += f"\n[DEBUG] Total posts calculado: {total_posts}, total examples: {len(all_examples)}"
        
        # Calculate engagement metrics
        total_likes = 0
        total_comments = 0
        total_views = 0
        
        for example in all_examples:
            if isinstance(example, dict):
                # Handle fields from the actual API structure
                likes = example.get('likes', 0) or 0
                comments = (example.get('respuestas', 0) or 
                           example.get('comentarios', 0) or 
                           example.get('comments', 0) or 0)
                views = (example.get('vistas', 0) or 
                        example.get('views', 0) or 0)
                
                # Also get other interactions
                retweets = example.get('retweets', 0) or 0
                guardados = example.get('guardados', 0) or 0
                
                total_likes += likes
                total_comments += comments + retweets  # Include retweets as comments
                total_views += views
                
                self.log_ejecucion += f"\n[DEBUG] Post: likes={likes}, respuestas={comments}, retweets={retweets}, views={views}"
        
        # Calculate average engagement rate
        avg_engagement = 0.0
        if total_posts > 0 and total_views > 0:
            avg_engagement = ((total_likes + total_comments) / total_views) * 100
        elif total_posts > 0 and (total_likes + total_comments) > 0:
            avg_engagement = (total_likes + total_comments) / total_posts
        
        self.log_ejecucion += f"\n[DEBUG] Métricas finales: likes={total_likes}, comments={total_comments}, views={total_views}, engagement={avg_engagement}"
        
        return {
            "total_clusters": total_clusters,
            "total_posts": total_posts,
            "avg_engagement_rate": round(avg_engagement, 4),
            "total_likes": total_likes,
            "total_comments": total_comments,
            "total_views": total_views,
            "cluster_sizes": cluster_sizes,
            "cluster_names": cluster_names,
            "summary_text": f"{total_clusters} clusters encontrados con {total_posts} publicaciones total",
            "modelo_usado": api_result.get('modelo_usado', 'N/A'),
            "details": {
                "avg_posts_per_cluster": round(total_posts / total_clusters, 2) if total_clusters > 0 else 0,
                "max_cluster_size": max(cluster_sizes) if cluster_sizes else 0,
                "min_cluster_size": min(cluster_sizes) if cluster_sizes else 0
            }
        }

    def _generate_fallback_summary(self, result_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary when clustering structure is unexpected"""
        self.log_ejecucion += f"\n[DEBUG] Fallback - analizando estructura: {list(result_data.keys()) if isinstance(result_data, dict) else type(result_data)}"
        
        # Try to extract meaningful data from unexpected structure
        total_clusters = 0
        total_posts = 0
        raw_keys = []
        
        if isinstance(result_data, dict):
            raw_keys = list(result_data.keys())
            
            # Try to find total_clusters in the data
            total_clusters = result_data.get('total_clusters', 0)
            
            # Try different ways to find cluster data
            possible_cluster_data = []
            
            for key in ['clusters', 'data', 'results', 'cluster_data']:
                if key in result_data and isinstance(result_data[key], list):
                    possible_cluster_data = result_data[key]
                    self.log_ejecucion += f"\n[DEBUG] Fallback - encontrados datos en '{key}': {len(possible_cluster_data)} elementos"
                    break
            
            # If we found cluster data, try to count posts
            if possible_cluster_data:
                total_clusters = len(possible_cluster_data)
                for item in possible_cluster_data:
                    if isinstance(item, dict):
                        # Look for posts in various field names (prioritizing the actual structure)
                        for post_key in ['publicaciones', 'ejemplos', 'posts', 'examples']:
                            if post_key in item and isinstance(item[post_key], list):
                                post_count = len(item[post_key])
                                total_posts += post_count
                                self.log_ejecucion += f"\n[DEBUG] Fallback - encontradas {post_count} publicaciones en campo '{post_key}'"
                                break
            
            # If still no clusters found, try to infer from keys
            if total_clusters == 0:
                # Count keys that might represent clusters
                cluster_like_keys = [k for k in raw_keys if k.startswith('cluster') or k.isdigit()]
                if cluster_like_keys:
                    total_clusters = len(cluster_like_keys)
                    self.log_ejecucion += f"\n[DEBUG] Fallback - inferidos {total_clusters} clusters de keys: {cluster_like_keys}"
        
        return {
            "total_clusters": total_clusters,
            "total_posts": total_posts,
            "avg_engagement_rate": 0.0,
            "total_likes": 0,
            "total_comments": 0,
            "total_views": 0,
            "cluster_sizes": [0] * total_clusters if total_clusters > 0 else [],
            "cluster_names": [f"Cluster {i}" for i in range(total_clusters)] if total_clusters > 0 else [],
            "summary_text": f"Estructura no estándar procesada: {total_clusters} clusters, {total_posts} posts",
            "raw_keys": raw_keys,
            "modelo_usado": result_data.get('modelo_usado', 'N/A') if isinstance(result_data, dict) else 'N/A'
        }

    @frappe.whitelist()
    def descargar_resultados_completos(self):
        """Generate download for complete clustering results"""
        try:
            if not self.resultado_clustering and not self.datos_raw:
                frappe.throw("No hay datos de clustering disponibles para descargar")
            
            # Prepare comprehensive download data
            download_data = {
                "metadata": {
                    "titulo": self.titulo,
                    "usuario": self.usuario_red_social,
                    "plataforma": self.plataforma_social,
                    "tipo_analisis": self.tipo_analisis,
                    "fecha_analisis": str(self.fecha_analisis) if self.fecha_analisis else None,
                    "fecha_creacion": str(self.fecha_creacion) if self.fecha_creacion else None,
                    "fecha_descarga": datetime.now().isoformat(),
                    "estado": self.estado,
                    "cluster_asignado": self.cluster_asignado,
                    "cluster_nombre": self.cluster_nombre
                },
                "resumen_ejecutivo": json.loads(self.resumen_clusters) if self.resumen_clusters else {},
                "clustering_detallado": json.loads(self.resultado_clustering) if self.resultado_clustering else {},
                "respuesta_api_completa": json.loads(self.datos_raw) if self.datos_raw else {},
                "log_ejecucion": self.log_ejecucion
            }
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"clustering_analysis_{self.usuario_red_social}_{timestamp}.json"
            
            # Return as downloadable JSON
            frappe.local.response.filename = filename
            frappe.local.response.filecontent = json.dumps(download_data, indent=2, ensure_ascii=False)
            frappe.local.response.type = "download"
            
            return {
                "success": True,
                "message": f"Archivo preparado para descarga: {filename}",
                "filename": filename,
                "size_kb": round(len(frappe.local.response.filecontent) / 1024, 2)
            }
            
        except Exception as e:
            frappe.throw(f"Error preparando descarga: {str(e)}")

    @frappe.whitelist()
    def obtener_resumen_detallado(self):
        """Get detailed summary for display in UI"""
        try:
            if not self.resumen_clusters:
                return {"error": "No hay resumen de clusters disponible"}
            
            summary_data = json.loads(self.resumen_clusters)
            
            # Add additional UI-friendly formatting
            ui_summary = {
                **summary_data,
                "cluster_asignado": self.cluster_asignado,
                "cluster_nombre": self.cluster_nombre,
                "estado_analisis": self.estado,
                "ultima_actualizacion": str(self.ultima_actualizacion) if self.ultima_actualizacion else None,
                "puede_descargar": bool(self.resultado_clustering or self.datos_raw)
            }
            
            return {"success": True, "data": ui_summary}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    @frappe.whitelist()
    def exportar_resultados(self):
        """Export analysis results to Excel/CSV"""
        pass

    def get_dashboard_data(self):
        """Get data for dashboard display"""
        if not self.datos_procesados:
            return {}
        
        try:
            data = json.loads(self.datos_procesados)
            return {
                "titulo": self.titulo,
                "estado": self.estado,
                "tipo_analisis": self.tipo_analisis,
                "plataforma": self.plataforma_social,
                "resumen": data.get("result", {}),
                "ultima_actualizacion": self.ultima_actualizacion
            }
        except:
            return {}


    def _format_clustering_display(self, summary: Dict[str, Any]) -> str:
        """Format clustering summary for user-friendly display"""
        if not summary:
            return "📋 No hay datos de clustering disponibles"
        
        try:
            display_text = f"""
═══════════════════════════════════════════════════════
                    ✨ RESUMEN DE CLUSTERING ✨
═══════════════════════════════════════════════════════

📊 ESTADÍSTICAS GENERALES:
   • Total de Clusters: {summary.get('total_clusters', 0)}
   • Total de Publicaciones: {summary.get('total_posts', 0)}
   • Tasa de Engagement Promedio: {summary.get('avg_engagement_rate', 0):.2f}%

💬 MÉTRICAS DE INTERACCIÓN:
   • Total de Likes: {summary.get('total_likes', 0):,}
   • Total de Comentarios: {summary.get('total_comments', 0):,}
   • Total de Visualizaciones: {summary.get('total_views', 0):,}

📈 DISTRIBUCIÓN DE CLUSTERS:
   • Tamaño de Clusters: {summary.get('cluster_sizes', [])}"""

            # Add details if available
            details = summary.get('details', {})
            if details:
                display_text += f"""
   • Publicaciones por Cluster (promedio): {details.get('avg_posts_per_cluster', 0)}
   • Cluster más grande: {details.get('max_cluster_size', 0)} publicaciones
   • Cluster más pequeño: {details.get('min_cluster_size', 0)} publicaciones"""

            display_text += "\n\n🏷️ CLUSTERS IDENTIFICADOS:"
            
            # Add cluster names if available
            cluster_names = summary.get('cluster_names', [])
            cluster_sizes = summary.get('cluster_sizes', [])
            
            if cluster_names and cluster_sizes:
                for i, name in enumerate(cluster_names):
                    size = cluster_sizes[i] if i < len(cluster_sizes) else 0
                    display_text += f"\n   • Cluster {i}: {name} ({size} publicaciones)"
            elif cluster_sizes:
                for i, size in enumerate(cluster_sizes):
                    display_text += f"\n   • Cluster {i}: {size} publicaciones"
            else:
                display_text += "\n   • No hay información detallada de clusters"
            
            display_text += f"""

🤖 INFORMACIÓN TÉCNICA:
   • Modelo Utilizado: {summary.get('modelo_usado', 'N/A')}
   • Fecha de Análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
   • Estado: ✅ Completado Exitosamente

═══════════════════════════════════════════════════════
            """
            
            return display_text.strip()
            
        except Exception as e:
            return f"❌ Error al formatear resumen de clustering: {str(e)}"

@frappe.whitelist()
def get_analisis_status(docname):
    """Obtener el estado actual del análisis"""
    try:
        doc = frappe.get_doc("Analisis Redes Sociales", docname)
        return {
            "estado": doc.estado,
            "error_message": doc.error_message,
            "log_ejecucion": doc.log_ejecucion
        }
    except Exception as e:
        return {"error": str(e)}

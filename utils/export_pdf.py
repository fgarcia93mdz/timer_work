# utils/export_pdf.py

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime, date, timedelta
import os

# Importar datos de la base de datos
try:
    from storage.database import obtener_estadisticas_diarias, obtener_resumen_semanal
except ImportError:
    print("⚠️ Módulo de base de datos no disponible para exportación")

def generar_reporte_diario(fecha=None, archivo_salida=None):
    """Genera un reporte PDF de la actividad diaria"""
    if fecha is None:
        fecha = date.today().isoformat()
    
    if archivo_salida is None:
        archivo_salida = f'storage/reporte_diario_{fecha}.pdf'
    
    try:
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(archivo_salida), exist_ok=True)
        
        # Configurar documento
        doc = SimpleDocTemplate(archivo_salida, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Título
        titulo_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.darkblue,
            spaceAfter=30,
            alignment=1  # Centrado
        )
        
        titulo = Paragraph(f"📊 REPORTE DIARIO DE ACTIVIDAD", titulo_style)
        fecha_formateada = datetime.strptime(fecha, '%Y-%m-%d').strftime('%d de %B de %Y')
        subtitulo = Paragraph(f"Fecha: {fecha_formateada}", styles['Heading2'])
        
        story.append(titulo)
        story.append(subtitulo)
        story.append(Spacer(1, 20))
        
        # Obtener datos
        try:
            estadisticas = obtener_estadisticas_diarias(fecha)
        except:
            estadisticas = None
        
        if estadisticas:
            # Sección de resumen general
            story.append(Paragraph("🎯 RESUMEN GENERAL", styles['Heading2']))
            
            resumen_data = [
                ['Métrica', 'Valor'],
                ['Tiempo total activo', f"{(estadisticas['estadisticas_generales'][2] or 0) // 3600}h {((estadisticas['estadisticas_generales'][2] or 0) % 3600) // 60}m"],
                ['Pomodoros completados', str(estadisticas['estadisticas_generales'][5] or 0)],
                ['Objetivos completados', str(estadisticas['estadisticas_generales'][6] or 0)],
                ['Aplicación principal', estadisticas['estadisticas_generales'][7] or 'N/A']
            ]
            
            tabla_resumen = Table(resumen_data)
            tabla_resumen.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(tabla_resumen)
            story.append(Spacer(1, 20))
            
            # Sección de tiempo por aplicaciones
            if estadisticas['tiempo_aplicaciones']:
                story.append(Paragraph("💻 TIEMPO POR APLICACIÓN", styles['Heading2']))
                
                apps_data = [['Aplicación', 'Tiempo (min)', 'Sesiones']]
                for app, tiempo, sesiones in estadisticas['tiempo_aplicaciones'][:10]:  # Top 10
                    tiempo_min = tiempo // 60
                    apps_data.append([app, str(tiempo_min), str(sesiones)])
                
                tabla_apps = Table(apps_data)
                tabla_apps.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(tabla_apps)
                story.append(Spacer(1, 20))
            
            # Sección de sesiones Pomodoro
            if estadisticas['sesiones_pomodoro']:
                story.append(Paragraph("🍅 SESIONES POMODORO", styles['Heading2']))
                
                pomodoro_data = [['Tipo de Sesión', 'Cantidad', 'Tasa de Éxito']]
                for tipo, cantidad, tasa in estadisticas['sesiones_pomodoro']:
                    tasa_porcentaje = f"{tasa * 100:.1f}%" if tasa else "0%"
                    pomodoro_data.append([tipo.replace('_', ' ').title(), str(int(cantidad)), tasa_porcentaje])
                
                tabla_pomodoro = Table(pomodoro_data)
                tabla_pomodoro.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.green),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(tabla_pomodoro)
                story.append(Spacer(1, 20))
        
        # Sección de recomendaciones
        story.append(Paragraph("💡 RECOMENDACIONES", styles['Heading2']))
        
        recomendaciones = [
            "• Mantén el ritmo de los Pomodoros para mejor concentración",
            "• Toma descansos regulares para evitar la fatiga",
            "• Identifica las horas más productivas del día",
            "• Reduce el tiempo en aplicaciones de distracción",
            "• Establece objetivos claros y medibles para el día siguiente"
        ]
        
        for rec in recomendaciones:
            story.append(Paragraph(rec, styles['Normal']))
        
        story.append(Spacer(1, 30))
        
        # Pie de página
        pie_pagina = Paragraph(
            f"Reporte generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}",
            styles['Normal']
        )
        story.append(pie_pagina)
        
        # Construir PDF
        doc.build(story)
        
        print(f"✅ Reporte PDF generado: {archivo_salida}")
        return archivo_salida
        
    except Exception as e:
        print(f"❌ Error al generar reporte PDF: {e}")
        return None

def generar_reporte_semanal(archivo_salida=None):
    """Genera un reporte PDF de la actividad semanal"""
    if archivo_salida is None:
        fecha_actual = date.today().isoformat()
        archivo_salida = f'storage/reporte_semanal_{fecha_actual}.pdf'
    
    try:
        # Configurar documento
        doc = SimpleDocTemplate(archivo_salida, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Título
        titulo = Paragraph("📈 REPORTE SEMANAL DE ACTIVIDAD", styles['Title'])
        story.append(titulo)
        story.append(Spacer(1, 20))
        
        # Obtener datos semanales
        try:
            datos_semanales = obtener_resumen_semanal()
        except:
            datos_semanales = []
        
        if datos_semanales:
            # Tabla de resumen semanal
            story.append(Paragraph("📊 RESUMEN DE LOS ÚLTIMOS 7 DÍAS", styles['Heading2']))
            
            tabla_data = [['Fecha', 'Tiempo Activo (h)', 'Pomodoros', 'Objetivos', 'App Principal']]
            
            total_tiempo = 0
            total_pomodoros = 0
            total_objetivos = 0
            
            for fila in datos_semanales:
                fecha_str = datetime.strptime(fila[0], '%Y-%m-%d').strftime('%d/%m')
                tiempo_horas = (fila[1] or 0) / 3600
                pomodoros = fila[2] or 0
                objetivos = fila[3] or 0
                app_principal = fila[4] or 'N/A'
                
                total_tiempo += tiempo_horas
                total_pomodoros += pomodoros
                total_objetivos += objetivos
                
                tabla_data.append([
                    fecha_str, 
                    f"{tiempo_horas:.1f}", 
                    str(pomodoros), 
                    str(objetivos), 
                    app_principal[:15]  # Truncar nombre largo
                ])
            
            # Fila de totales
            tabla_data.append([
                'TOTAL', 
                f"{total_tiempo:.1f}", 
                str(total_pomodoros), 
                str(total_objetivos), 
                ''
            ])
            
            tabla_semanal = Table(tabla_data)
            tabla_semanal.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.navy),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -2), colors.lightblue),
                ('BACKGROUND', (0, -1), (-1, -1), colors.yellow),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(tabla_semanal)
            story.append(Spacer(1, 30))
            
            # Análisis y métricas
            story.append(Paragraph("📈 ANÁLISIS SEMANAL", styles['Heading2']))
            
            promedio_diario_tiempo = total_tiempo / 7
            promedio_diario_pomodoros = total_pomodoros / 7
            
            analisis = [
                f"• Promedio diario de tiempo activo: {promedio_diario_tiempo:.1f} horas",
                f"• Promedio diario de Pomodoros: {promedio_diario_pomodoros:.1f}",
                f"• Total de objetivos completados: {total_objetivos}",
                f"• Productividad general: {'Excelente' if promedio_diario_tiempo > 6 else 'Buena' if promedio_diario_tiempo > 4 else 'Mejorable'}"
            ]
            
            for item in analisis:
                story.append(Paragraph(item, styles['Normal']))
        
        story.append(Spacer(1, 30))
        
        # Pie de página
        pie_pagina = Paragraph(
            f"Reporte semanal generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}",
            styles['Normal']
        )
        story.append(pie_pagina)
        
        # Construir PDF
        doc.build(story)
        
        print(f"✅ Reporte semanal PDF generado: {archivo_salida}")
        return archivo_salida
        
    except Exception as e:
        print(f"❌ Error al generar reporte semanal: {e}")
        return None

def exportar_csv_actividad(fecha=None):
    """Exporta los datos de actividad a formato CSV"""
    if fecha is None:
        fecha = date.today().isoformat()
    
    archivo_csv = f'storage/actividad_{fecha}.csv'
    
    try:
        # Aquí podrías implementar exportación a CSV
        # usando los datos de la base de datos
        print(f"📄 Exportación CSV implementar en: {archivo_csv}")
        return archivo_csv
    except Exception as e:
        print(f"❌ Error al exportar CSV: {e}")
        return None

if __name__ == "__main__":
    # Prueba de generación de reportes
    print("Generando reporte de prueba...")
    generar_reporte_diario()
    generar_reporte_semanal()

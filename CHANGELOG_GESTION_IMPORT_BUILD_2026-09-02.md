# L-26 V27.3.10 — Gestión, importación y empaquetado

## Gestión / Trámites
- Se separa la importación de ZIP de Gestión del importador de Trámites.
- Un ZIP con esquema `FiscalizacionBIManagementExport` o `gestiones.json` ya no puede ser absorbido desde Trámites.
- El importador de Gestión fuerza los expedientes restaurados a permanecer en Gestión, incluso cuando el respaldo antiguo carece de metadatos completos de etapa.
- Se agrega **Cargar Excel** en Gestión para archivos XLSX/CSV usando el mismo reconocimiento y deduplicación por Folio ya existente.
- Los registros cargados por Excel desde Gestión quedan marcados con destino `management` y no vuelven a la lista de Trámites activos.

## Windows / Android
- La distribución oficial continúa limitada a Windows y Android; no se añade objetivo Linux.
- Se corrige `desktop/BUILD_WINDOWS.cmd`, que todavía mostraba nombres de salida 26.0.0.
- Se agregan reintentos y tiempos de espera de npm para reducir fallos transitorios DNS/EAI_AGAIN durante la descarga de Electron.
- El vendorizado de PDF.js reintenta cada origen hasta tres veces antes de abortar, mejorando la creación del APK y del instalador Windows cuando hay fallos temporales de red.
- Se mantienen AGP 9.3.0, Gradle 9.5.0 y JDK 17 para Android por ser una combinación compatible.

## Verificación
- Se añadieron pruebas de regresión específicas para separación Gestión/Trámites y endurecimiento de instaladores.

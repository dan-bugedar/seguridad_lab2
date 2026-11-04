# Evidencias del laboratorio 2 versión 2.1

Participante: Daniela Bugeda  Fecha: 29 octubre 2026

No incluyas claves, tokens ni datos recuperados. Escribe los resultados observados, no solo los esperados.

## Preparación y comprobaciones

Resultado de comprobar_preparacion_lab2.py: 

Preparacion verificada: datos, referencia, clave y TODO 1 a 4
No se han creado salidas ni mostrado claves o datos personales

Resultado de comprobar_lab2.py --todo 5: 

TODO 5 OK: tres eventos anexados con campos exactos y fecha UTC.
Etapa TODO 5 verificada; no valida las otras funciones.

Resultado de comprobar_lab2.py --todo 6: 

TODO 6 OK: resumen valido aceptado y ocho casos invalidos rechazados.
Etapa TODO 6 verificada; no valida las otras funciones.

Resultado de comprobar_lab2.py --todo 7: 

TODO 7 OK: traza valida aceptada y catorce casos invalidos rechazados.
Etapa TODO 7 verificada; no valida las otras funciones.

Resultado de comprobar_lab2.py completo: 

TODO 5 OK: tres eventos anexados con campos exactos y fecha UTC.
TODO 6 OK: resumen valido aceptado y ocho casos invalidos rechazados.
TODO 7 OK: traza valida aceptada y catorce casos invalidos rechazados.
TODO 5, 6 y 7 verificados. Continua con la auditoria completa.

## Auditoría válida

RUN_ID: 3ce7d7486dcc4c3f945ea37583fc0a02

Ruta de reporte.json: ejecuciones/3ce7d7486dcc4c3f945ea37583fc0a02/reporte.json

Ruta de eventos.jsonl: ejecuciones/3ce7d7486dcc4c3f945ea37583fc0a02/eventos.jsonl

| Control | Estado observado | Evidencia concreta |
| --- | --- | --- |
| INTEGRIDAD | SATISFACTORIO | hash_entrada del reporte |
| CIFRADO | SATISFACTORIO | alidas/detalle_protegido.csv |
| MINIMIZACION | SATISFACTORIO | salidas/resumen.csv |
| ACCESO_DENEGADO | SATISFACTORIO | eventos.jsonl |
| TRAZABILIDAD | SATISFACTORIO | eventos.jsonl |

Filas de detalle: 13  Filas de resumen: 4

Totales por ciudad y total general: 

Merida,4000.00
Puebla,2500.00
Villahermosa,4250.00
Total General,10750.00

## Escenarios negativos

| Escenario | RUN_ID o ruta | Estados y resultado observados | Acción propuesta |
| --- | --- | --- | --- |
| A Entrada alterada |ejecuciones/d1ae8500742b44c7950d912e1c49e617 | INTEGRIDAD y EJECUCION **FALLIDO**; CIFRADO, MINIMIZACION, ACCESO_DENEGADO y TRAZABILIDAD **NO_EVALUADO** | Mantener la referencia original y revisar el origen del archivo. No procesar información cuya integridad no pudo verificarse. |
| B Analista intenta ejecutar | ejecuciones/ef614c78c997432eb79f9a99d43ab9ef|AUTORIZACION_INICIAL y EJECUCION **FALLIDO**, el resto **NO_EVALUADO** | Mantener la restricción de permisos y permitir la ejecución únicamente a los roles autorizados. |
| C Analista intenta consultar | No genera RUN_ID | PermissionError('Operacion no autorizada para el rol') | Mantener el control de autorización para impedir que usuarios sin permiso accedan al reporte. |
| D Pruebas aisladas | Archivos temporales | | 	Conservar los resultados de las pruebas que verifican que los casos válidos son aceptados y los inválidos rechazados. |

¿Se crearon salidas del pipeline en A o B? No. En ambos escenarios se bloqueó la ejecución antes de generar los archivos de salida. Esto evita que se procese información alterada o que una operación sea realizada por un rol no autorizado.

¿Qué controles quedaron NO_EVALUADO y por qué? En el escenario A quedaron sin evaluar CIFRADO, MINIMIZACIÓN, ACCESO_DENEGADO y TRAZABILIDAD. En el escenario B, los cinco controles previstos quedaron sin evaluar. Esto ocurrió porque la ejecución se detuvo antes de llegar a esas comprobaciones, ya sea por una falla de integridad o por falta de autorización.

## Hallazgo y explicación

Qué ocurrió: Se implementaron controles de seguridad para proteger la información de los pedidos y auditar las operaciones del pipeline. Durante la auditoría válida, el sistema permitió la ejecución del operador y verificó satisfactoriamente los controles de integridad, cifrado, minimización, acceso denegado y trazabilidad. En las pruebas negativas, el sistema identificó correctamente los intentos de procesar un archivo alterado y de ejecutar operaciones con un rol sin permisos.

Qué control actuó: Actuaron distintos controles dependiendo del escenario: SHA-256 para verificar la integridad del archivo original, Fernet para proteger los datos personales, autorización basada en roles para restringir operaciones, minimización para limitar los campos del resumen y registro de eventos JSONL para mantener la trazabilidad de las operaciones.

Dónde está la evidencia: La evidencia se encuentra en los archivos reporte.json y eventos.jsonl de cada ejecución, así como en los archivos generados dentro de la carpeta salidas para la auditoría válida. También se cuenta con los resultados de las pruebas automatizadas de los TODO 5, 6 y 7.

Qué corregirías: Para un entorno de producción, incorporaría autenticación real de usuarios, una administración centralizada de permisos y almacenamiento seguro de claves. También protegería los registros de auditoría contra modificaciones, agregaría monitoreo y definiría políticas de conservación y respaldo de la información.

Qué no demuestra este laboratorio: Este laboratorio demuestra el funcionamiento de controles técnicos específicos en un entorno local y con datos ficticios. No demuestra la identidad real de quien ejecuta las operaciones, ni garantiza que los archivos de auditoría sean inalterables. 

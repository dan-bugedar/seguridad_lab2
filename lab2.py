import argparse
import csv
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
import lab1

BASE = Path(__file__).resolve().parent


def registrar_evento(ruta, run_id, rol, operacion, resultado):
    # Obtener la fecha y hora actual en UTC.
    fecha_utc = datetime.now(timezone.utc).isoformat()

    # Crear el registro con los campos requeridos.
    evento = {
        "run_id": run_id,
        "fecha_utc": fecha_utc,
        "rol": rol,
        "operacion": operacion,
        "resultado": resultado
    }

    # Anexar el evento al archivo en formato JSON Lines.
    with open(ruta, "a", encoding="utf-8") as archivo:
        archivo.write(json.dumps(evento, ensure_ascii=False) + "\n")


def comprobar_minimizacion(ruta):
    try:
        with open(ruta, "r", encoding="utf-8", newline="") as archivo:
            lector = csv.reader(archivo)

            encabezados = next(lector, None)

            if encabezados != ["ciudad", "total_ventas"]:
                return False

            filas = list(lector)

            if not filas:
                return False

            for fila in filas:
                if len(fila) != 2:
                    return False

                if not all(valor.strip() for valor in fila):
                    return False

            return True

    except (OSError, UnicodeError, csv.Error):
        return False


def comprobar_trazabilidad(ruta, run_id):
    campos = {
        "run_id",
        "fecha_utc",
        "rol",
        "operacion",
        "resultado"
    }

    eventos_esperados = {
        ("operador", "ejecutar", "PERMITIDO"),
        ("operador", "pipeline", "COMPLETADO"),
        ("analista", "ejecutar", "DENEGADO")
    }

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

        if not lineas:
            return False

        eventos_encontrados = set()

        for linea in lineas:
            if not linea.strip():
                return False

            evento = json.loads(linea)

            if not isinstance(evento, dict):
                return False

            if set(evento.keys()) != campos:
                return False

            if not all(
                isinstance(valor, str) and valor.strip()
                for valor in evento.values()
            ):
                return False

            if evento["run_id"] != run_id:
                return False

            fecha = datetime.fromisoformat(evento["fecha_utc"])

            if fecha.tzinfo is None:
                return False

            if fecha.utcoffset() != timezone.utc.utcoffset(fecha):
                return False

            registro = (
                evento["rol"],
                evento["operacion"],
                evento["resultado"]
            )

            if registro in eventos_esperados:
                eventos_encontrados.add(registro)

        return eventos_encontrados == eventos_esperados

    except (OSError, UnicodeError, json.JSONDecodeError,
            ValueError, TypeError):
        return False


def comprobar_cifrado(detalle, entrada):
    originales = lab1.leer_pedidos(entrada)
    protegidas = lab1.leer_pedidos(detalle)
    if len(originales) != len(protegidas):
        return False
    fernet = lab1.cargar_cifrador()
    for original, protegida in zip(originales, protegidas):
        if original['pedido_id'] != protegida['pedido_id']:
            return False
        for campo in ('nombre_cliente', 'correo'):
            token = protegida[campo]
            if token == original[campo]:
                return False
            if lab1.descifrar(token, fernet) != original[campo]:
                return False
    return True


def auditar(rol, entrada, referencia):
    run_id = uuid.uuid4().hex
    carpeta = BASE / 'ejecuciones' / run_id
    carpeta.mkdir(parents=True, exist_ok=False)
    eventos = carpeta / 'eventos.jsonl'
    controles = []

    def agregar(control, estado, evidencia, accion=''):
        controles.append({
            'control': control, 'estado': estado,
            'evidencia': evidencia, 'accion': accion,
        })

    def revisar(control, funcion, evidencia):
        try:
            ok = funcion()
            agregar(control, 'SATISFACTORIO' if ok else 'FALLIDO',
                    evidencia, '' if ok else 'Investigar control')
        except NotImplementedError:
            agregar(control, 'NO_EVALUADO', evidencia,
                    'Completar TODO correspondiente')
        except Exception as exc:
            agregar(control, 'FALLIDO', evidencia,
                    f'Revisar {type(exc).__name__}')

    try:
        try:
            lab1.autorizar(rol, 'ejecutar')
        except PermissionError:
            registrar_evento(eventos, run_id, rol,
                             'ejecutar', 'DENEGADO')
            agregar('AUTORIZACION_INICIAL', 'FALLIDO',
                    'eventos.jsonl', 'Usar operador')
            raise
        registrar_evento(eventos, run_id, rol,
                         'ejecutar', 'PERMITIDO')
        # No se escribe salida si no coincide la referencia.
        try:
            lab1.verificar_integridad(entrada, referencia)
        except ValueError:
            agregar('INTEGRIDAD', 'FALLIDO',
                    'Comparacion con referencia confiable',
                    'Revisar origen del archivo; no procesar')
            raise
        agregar('INTEGRIDAD', 'SATISFACTORIO',
                'hash_entrada del reporte')
        resultado = lab1.ejecutar(
            rol, entrada, referencia, carpeta / 'salidas')
        registrar_evento(eventos, run_id, rol,
                         'pipeline', 'COMPLETADO')
        revisar('CIFRADO', lambda: comprobar_cifrado(
            resultado['detalle'], entrada),
            'salidas/detalle_protegido.csv')
        revisar('MINIMIZACION', lambda: comprobar_minimizacion(
            resultado['resumen']), 'salidas/resumen.csv')
        try:
            lab1.autorizar('analista', 'ejecutar')
        except PermissionError:
            registrar_evento(eventos, run_id, 'analista',
                             'ejecutar', 'DENEGADO')
            agregar('ACCESO_DENEGADO', 'SATISFACTORIO',
                    'eventos.jsonl')
        else:
            agregar('ACCESO_DENEGADO', 'FALLIDO',
                    'No se produjo PermissionError',
                    'Corregir autorizar antes de continuar')
        revisar('TRAZABILIDAD', lambda: comprobar_trazabilidad(
            eventos, run_id), 'eventos.jsonl')
    except NotImplementedError:
        agregar('EJECUCION', 'NO_EVALUADO', 'Codigo base',
                'Completar TODO 1 a 5 antes de continuar')
    except Exception as exc:
        agregar('EJECUCION', 'FALLIDO', type(exc).__name__,
                'Revisar permisos, integridad y entorno')
    presentes = {c['control'] for c in controles}
    for nombre in ('INTEGRIDAD', 'CIFRADO', 'MINIMIZACION',
                   'ACCESO_DENEGADO', 'TRAZABILIDAD'):
        if nombre not in presentes:
            agregar(nombre, 'NO_EVALUADO', 'Sin ejecucion',
                    'Resolver bloqueo y repetir en nueva carpeta')
    reporte = {
        'run_id': run_id,
        'fecha_utc': datetime.now(timezone.utc).isoformat(),
        'rol_ejecutor': rol,
        'hash_entrada': lab1.calcular_hash(entrada)
            if 'SATISFACTORIO' in [
                c['estado'] for c in controles
                if c['control'] == 'INTEGRIDAD'] else None,
        'controles': controles,
    }
    ruta = carpeta / 'reporte.json'
    ruta.write_text(json.dumps(reporte, indent=2,
                              ensure_ascii=False), encoding='utf-8')
    # Ruta e identificador; nunca contenido personal o claves.
    print(f'Reporte generado: {ruta}')
    return ruta


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('accion', choices=['ejecutar', 'consultar'])
    parser.add_argument('--rol', default='operador')
    parser.add_argument('--entrada', type=Path,
                        default=lab1.DATOS / 'pedidos.csv')
    parser.add_argument('--referencia', type=Path,
                        default=BASE / 'referencia.sha256')
    parser.add_argument('--reporte', type=Path)
    args = parser.parse_args()
    if args.accion == 'ejecutar':
        auditar(args.rol, args.entrada, args.referencia)
    else:
        lab1.autorizar(args.rol, 'evidencias')
        if not args.reporte:
            parser.error('consultar requiere --reporte RUTA')
        print(args.reporte.read_text(encoding='utf-8'))


if __name__ == '__main__':
    main()

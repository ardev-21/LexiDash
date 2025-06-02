import pandas as pd
import random
from faker import Faker
from datetime import date, timedelta
import logging
from pathlib import Path
from typing import List, Dict, Any

# Configuración de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

# Configuración
fake = Faker("es_ES")
random.seed(42)

# Parámetros globales
GENERO = ["Masculino", "Femenino", "Otro"]
ESTADO_CIVIL = ["Soltero", "Casado", "Divorciado", "Viudo"]
EDAD_MINIMA_LABORAL = 18
ESTADO_CASO = ["Abierto", "Cerrado", "En proceso"]
ESTADO = ["Activo", "Inactivo", "En licencia"]
ROL = ["Cliente", "Abogado", "Testigo"]
TIPO_AUDIENCIA = ["Preliminar", "Intermedia", "Juicio", "Apelación"]
TIPO_DOCUMENTO = ["Demanda", "Escrito de defensa", "Prueba", "Resolución"]
TIPO_RESOLUCION = [
    "Sentencia Condenatoria",
    "Sentencia Absolutoria",
    "Acuerdo Extrajudicial",
    "Conciliación Judicial",
    "Mediación Exitosa",
    "Archivo por Falta de Pruebas",
    "Sobreseimiento",
    "Desistimiento del Demandante",
    "Resolución Administrativa",
    "Recurso Concedido",
    "Recurso Denegado",
    "Multa o Sanción",
    "Caso en Curso",
]
RESULTADOS = ["Ganado", "Perdido", "Acuerdo"]
TIPOS_OTROS_RECURSOS = [
    "Peritaje",
    "Traducción de documentos",
    "Notificaciones",
    "Copias certificadas",
    "Gastos de mensajería",
    "Honorarios de testigos",
    "Desplazamientos",
    "Tasas judiciales",
    "Consultoría externa",
    "Gastos de archivo",
    "Gastos de investigación",
    "Gastos de mediación",
    "Gastos de conciliación",
    "Gastos de digitalización",
    "Gastos de correspondencia",
]
# Diccionario de ramas legales y tipos
RAMAS_LEGALES_Y_TIPOS = {
    "Penal": [
        "Robo o hurto",
        "Homicidio",
        "Lesiones personales",
        "Violencia de género",
        "Fraude",
        "Narcotráfico",
        "Delitos informáticos",
    ],
    "Civil": [
        "Incumplimiento de contrato",
        "Daños y perjuicios",
        "Reclamación por deuda",
        "Propiedad y posesión",
        "Arrendamientos",
        "Sucesiones y herencias",
    ],
    "Laboral": [
        "Despido injustificado",
        "Acoso laboral",
        "Reclamación de salarios",
        "Reinstalación",
        "Negociación colectiva",
        "Accidente de trabajo",
    ],
    "Mercantil": [
        "Incumplimiento comercial",
        "Contratos mercantiles",
        "Quiebra o insolvencia",
        "Conflictos societarios",
        "Competencia desleal",
        "Registro de marca",
    ],
    "Administrativo": [
        "Sanción administrativa",
        "Licencias y permisos",
        "Recursos administrativos",
        "Multas municipales",
        "Responsabilidad patrimonial del Estado",
        "Contratación pública",
    ],
    "Constitucional": [
        "Acción de amparo",
        "Acción de tutela",
        "Inconstitucionalidad de norma",
        "Violación de derechos fundamentales",
        "Habeas corpus",
        "Conflicto de competencias",
    ],
    "Internacional Público": [
        "Litigio entre Estados",
        "Derechos humanos",
        "Extradición",
        "Tratado internacional",
        "Refugiados y asilo",
        "Conflictos fronterizos",
    ],
    "Internacional Privado": [
        "Conflicto de leyes",
        "Divorcio internacional",
        "Contrato internacional",
        "Herencia transnacional",
        "Adopción internacional",
        "Reconocimiento de sentencias extranjeras",
    ],
    "Ambiental": [
        "Contaminación",
        "Evaluación de impacto ambiental",
        "Daño ecológico",
        "Sanción ambiental",
        "Licencia ambiental",
        "Protección de áreas naturales",
    ],
    "Procesal": [
        "Recurso de apelación",
        "Nulidad procesal",
        "Ejecución de sentencia",
        "Competencia jurisdiccional",
        "Medidas cautelares",
        "Revisión judicial",
    ],
    "Familia": [
        "Divorcio",
        "Custodia de menores",
        "Manutención",
        "Adopción",
        "Tutela o curatela",
        "Violencia intrafamiliar",
    ],
    "Notarial y Registral": [
        "Escritura pública",
        "Constitución de sociedad",
        "Testamento",
        "Legalización de documentos",
        "Registro de propiedad",
        "Actos de compraventa",
    ],
    "Seguridad Social": [
        "Reclamación de pensión",
        "Subsidio por enfermedad",
        "Cotización incorrecta",
        "Incapacidad permanente",
        "Afiliación al sistema",
        "Reintegro de prestaciones",
    ],
    "Informático": [
        "Delito informático",
        "Protección de datos personales",
        "Ciberacoso",
        "Suplantación digital",
        "Hackeo o intrusión",
        "Contrato de software",
    ],
}


def generar_nombre(genero: str) -> str:
    if genero == "Masculino":
        return f"{fake.first_name_male()} {fake.last_name()}"
    elif genero == "Femenino":
        return f"{fake.first_name_female()} {fake.last_name()}"
    return f"{fake.first_name()} {fake.last_name()}"


def edad_y_antiguedad() -> tuple[int, int]:
    edad = random.randint(25, 70)
    antiguedad = random.randint(0, max(0, edad - EDAD_MINIMA_LABORAL))
    return edad, antiguedad


class GeneradorDatosJudiciales:
    def __init__(self, num_casos: int, num_clientes: int):
        self.num_casos = num_casos
        self.num_clientes = num_clientes
        self.abogados: List[Dict[str, Any]] = []
        self.clientes: List[Dict[str, Any]] = []
        self.casos: List[Dict[str, Any]] = []
        self.facturacion: List[Dict[str, Any]] = []
        self.recursos: List[Dict[str, Any]] = []
        self.audiencias: List[Dict[str, Any]] = []
        self.documentos: List[Dict[str, Any]] = []
        self.comentarios: List[Dict[str, Any]] = []
        self.asistencias: List[Dict[str, Any]] = []
        self.resoluciones: List[Dict[str, Any]] = []
        self.abogados_por_rama: Dict[str, List[int]] = {}

    def generar_abogados(self):
        logging.info("Generando abogados...")
        id_abogado = 1
        for rama, tipos in RAMAS_LEGALES_Y_TIPOS.items():
            self.abogados_por_rama[rama] = []
            num_abogados_en_rama = random.randint(2, 5)
            for _ in range(num_abogados_en_rama):
                genero_elegido = random.choices(GENERO, weights=[0.47, 0.47, 0.06])[0]
                nombre_generado = generar_nombre(genero_elegido)
                edad, antiguedad = edad_y_antiguedad()
                abogado = {
                    "ID Abogado": id_abogado,
                    "Nombre": nombre_generado,
                    "Edad": edad,
                    "Rama Legal": rama,
                    "Género": genero_elegido,
                    "Años de Experiencia": antiguedad,
                    "Especialización": random.choice(tipos),
                    "Contacto": fake.phone_number(),
                    "Email": fake.email(),
                    "Estado": random.choice(ESTADO),
                }
                self.abogados.append(abogado)
                self.abogados_por_rama[rama].append(id_abogado)
                id_abogado += 1

    def generar_clientes(self):
        logging.info("Generando clientes...")
        for i in range(1, self.num_clientes + 1):
            genero_elegido = random.choices(GENERO, weights=[0.48, 0.48, 0.04])[0]
            nombre_generado = generar_nombre(genero_elegido)
            edad, antiguedad = edad_y_antiguedad()

            self.clientes.append(
                {
                    "ID Cliente": i,
                    "Nombre": nombre_generado,
                    "Edad": edad,
                    "Género": genero_elegido,
                    "Domicilio": fake.address(),
                    "Teléfono": fake.phone_number(),
                    "Email": fake.email(),
                    "Puesto": fake.job(),
                    "Estado Civil": random.choice(ESTADO_CIVIL),
                    "Antigüedad (años)": antiguedad,
                }
            )

    def generar_casos(self):
        logging.info("Generando casos...")
        for i in range(1, self.num_casos + 1):
            rama = random.choice(list(RAMAS_LEGALES_Y_TIPOS))
            abogado_activo = [
                ab["ID Abogado"]
                for ab in self.abogados
                if ab["Rama Legal"] == rama and ab["Estado"] == "Activo"
            ]
            if not abogado_activo:
                abogado_activo = [
                    ab["ID Abogado"] for ab in self.abogados if ab["Rama Legal"] == rama
                ]
            abogado_id = random.choice(abogado_activo)
            cliente = random.choice(self.clientes)
            fecha_inicio = fake.date_between(start_date="-5y", end_date="-1y")
            fecha_resolucion = fake.date_between(
                start_date=fecha_inicio, end_date="today"
            )
            estado = random.choice(ESTADO_CASO)
            resultado = (
                "Pendiente"
                if estado == "Abierto" or estado == "En proceso"
                else random.choice(RESULTADOS)
            )
            self.casos.append(
                {
                    "ID Caso": i,
                    "ID Cliente": cliente["ID Cliente"],
                    "ID Abogado": abogado_id,
                    "Descripción": fake.sentence(),
                    "Estado": estado,
                    "Fecha de Inicio": fecha_inicio,
                    "Fecha de Resolución": fecha_resolucion,
                    "Rama Legal": rama,
                    "Resultado": resultado,
                    "Tipo de Caso": random.choice(RAMAS_LEGALES_Y_TIPOS[rama]),
                }
            )

    def generar_facturacion_y_recursos(self):
        logging.info("Generando facturación y recursos...")
        for caso in self.casos:
            tarifa = round(random.uniform(50, 300), 2)
            horas = random.randint(5, 100)
            fecha_fact = fake.date_between(
                caso["Fecha de Inicio"], caso["Fecha de Resolución"]
            )

            fecha_pago = (
                fake.date_between(fecha_fact, caso["Fecha de Resolución"])
                if caso["Estado"] == "Cerrado"
                else None
            )

            if fecha_pago:
                pagos = round(tarifa * horas, 2)
                deuda = 0.0
            else:
                pagos = round(random.uniform(0, tarifa * horas), 2)
                deuda = round((tarifa * horas) - pagos, 2)

            if deuda > 0 and caso["Estado"] == "Cerrado":
                caso["Estado"] = random.choice(["Abierto", "En proceso"])

            self.facturacion.append(
                {
                    "ID Caso": caso["ID Caso"],
                    "Fecha de Facturación": fecha_fact,
                    "Fecha de Pago": fecha_pago,
                    "Tarifa por Hora": tarifa,
                    "Deuda Pendiente": deuda,
                    "Pagos Recibidos": pagos,
                }
            )

            recursos = random.sample(TIPOS_OTROS_RECURSOS, random.randint(1, 5))
            montos = [round(random.uniform(50, 500), 2) for _ in recursos]
            self.recursos.append(
                {
                    "ID Caso": caso["ID Caso"],
                    "Horas Trabajadas": horas,
                    "Gastos Administrativos": round(random.uniform(100, 1000), 2),
                    "Otros Recursos": ", ".join(recursos),
                    "Monto Otros Recursos": sum(montos),
                    "Descripción": ", ".join(
                        f"{r}: ${m}" for r, m in zip(recursos, montos)
                    ),
                }
            )

    def generar_otros(self):
        logging.info(
            "Generando audiencias, documentos, comentarios, asistencias y resoluciones..."
        )
        for caso in self.casos:
            inicio, resolucion = caso["Fecha de Inicio"], caso["Fecha de Resolución"]

            fecha_audiencia = fake.date_between(
                inicio, date.today() + timedelta(days=365)
            )

            if caso["Estado"] == "Cerrado":
                fecha_audiencia = fake.date_between(inicio, resolucion)
                tipo_audiencia = "Juicio"
            elif caso["Estado"] == "En proceso":
                fecha_audiencia = fake.date_between(inicio, date.today())
                tipo_audiencia = "Intermedia"
            else:
                fecha_audiencia = fake.date_between(
                    date.today(), date.today() + timedelta(days=365)
                )
                tipo_audiencia = "Preliminar"

            self.audiencias.append(
                {
                    "ID Caso": caso["ID Caso"],
                    "Fecha de Audiencia": fecha_audiencia,
                    "Tipo de Audiencia": tipo_audiencia,
                    "Lugar": fake.city(),
                }
            )

            self.documentos.append(
                {
                    "ID Caso": caso["ID Caso"],
                    "Tipo de Documento": random.choice(TIPO_DOCUMENTO),
                    "Fecha de Emisión": fake.date_between(inicio, resolucion),
                    "Resumen": fake.text(max_nb_chars=100),
                }
            )

            self.comentarios.append(
                {
                    "ID Caso": caso["ID Caso"],
                    "Fecha": fake.date_between(inicio, resolucion),
                    "Autor": fake.name(),
                    "Comentario": fake.sentence(),
                }
            )

            self.asistencias.append(
                {
                    "ID Caso": caso["ID Caso"],
                    "Fecha": fake.date_between(inicio, resolucion),
                    "Participante": fake.name(),
                    "Rol": random.choice(ROL),
                }
            )

            tipo_resolucion = (
                random.choice(
                    [res for res in TIPO_RESOLUCION if res != "Caso en Curso"]
                )
                if caso["Estado"] == "Cerrado"
                else "Caso en Curso"
            )
            self.resoluciones.append(
                {
                    "ID Caso": caso["ID Caso"],
                    "Fecha de Resolución": resolucion,
                    "Contenido": fake.text(max_nb_chars=150),
                    "Tipo de Resolución": tipo_resolucion,
                }
            )

    def validar_coherencia(self):
        for caso in self.casos:
            if caso["Estado"] != "Cerrado" and caso["Resultado"] != "Pendiente":
                logging.warning(f"Incoherencia en resultado del caso {caso['ID Caso']}")
            if caso["Estado"] == "Cerrado":
                res = next(
                    (r for r in self.resoluciones if r["ID Caso"] == caso["ID Caso"]),
                    None,
                )
                if not res or res["Tipo de Resolución"] == "Caso en Curso":
                    logging.warning(
                        f"Resolución incoherente en caso cerrado {caso['ID Caso']}"
                    )

    def guardar_csv(self, ruta: str = "salida_csv"):
        logging.info("Guardando archivos CSV...")
        output_path = Path(ruta)
        output_path.mkdir(parents=True, exist_ok=True)
        archivos = {
            "abogados.csv": self.abogados,
            "clientes.csv": self.clientes,
            "casos.csv": self.casos,
            "facturacion.csv": self.facturacion,
            "recursos.csv": self.recursos,
            "audiencias.csv": self.audiencias,
            "documentos.csv": self.documentos,
            "comentarios.csv": self.comentarios,
            "asistencias.csv": self.asistencias,
            "resoluciones.csv": self.resoluciones,
        }
        for nombre_archivo, datos in archivos.items():
            pd.DataFrame(datos).to_csv(output_path / nombre_archivo, index=False)


if __name__ == "__main__":
    generador = GeneradorDatosJudiciales(
        num_casos=random.randint(5000, 10000), num_clientes=random.randint(1000, 5000)
    )
    generador.generar_abogados()
    generador.generar_clientes()
    generador.generar_casos()
    generador.generar_facturacion_y_recursos()
    generador.generar_otros()
    generador.validar_coherencia()
    generador.guardar_csv()
    logging.info("¡Todos los archivos se generaron correctamente!")

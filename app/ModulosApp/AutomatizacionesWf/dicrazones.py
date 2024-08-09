# -*- coding: utf-8 -*-

#RAZONADOR
x={"AMPLIACION DE TAP HFC":{"LETRA":"H"},
"AMPLIACION DE TAP FTTH":{"LETRA":"H"},
"CLIENTE AUN NO DESEA EL TRABAJO":{"LETRA":"7"},
"CLIENTE NO TIENE DINERO":{"LETRA":"O"},
"CLIENTE SOLICITA REPROGRAMAR":{"LETRA":"K"},
"DIRECCION Y/O DATOS ERRADOS":{"LETRA":"B"},
"DUCTOS/INFRESTRUCTURA PREDIO NO APTA":{"LETRA":"W"},
"EQUIPOS CLIENTE NO APTOS/NO DISPONIBLES":{"LETRA":"6"},
"FALTA DE MATERIALES/EQUIPOS":{"LETRA":"F"},
"FUERA DE ZONA/SIN COBERTURA DE RED":{"LETRA":"Z"},
"INSTALACIÓN REQUIERE ANDAMIO ARNES":{"LETRA":"Y"},
"LLUVIA - FACTORES CLIMÁTICOS":{"LETRA":"L"},
"MAL AGENDADO/MAL PROGRAMADO":{"LETRA":"M"},
"NO INGRESO/CLIENTE CONFIRMA SERVICIO OK":{"LETRA":"S"},
"PERMISOS DE ADMINISTRACION":{"LETRA":"P"},
"PROBLEMA ORDEN PUBLICO/ZONA ROJA":{"LETRA":"X"},
"PROBLEMAS EN LA RED EXTERNA":{"LETRA":"%"},
"PROBLEMAS EN SISTEMAS APLICATIVOS CLARO":{"LETRA":"Q"},
"REPLANTEAMIENTO VT":{"LETRA":"R"},
"REQUIERE MOVIL ELITE":{"LETRA":"="},
"SUSCRIPTOR NO DESEA/NO REQUIERE TRABAJOS":{"LETRA":"E"},
"SUSCRIPTOR NO ESTA EN CONDICIÓN DE ATENDER":{"LETRA":"?"},
"UNIDAD POSIBLE FRAUDE":{"LETRA":"V"},
"VENTA DEVUELTA AL ASESOR":{"LETRA":"4"},
"NO CONTACTO CON CLIENTE":{"LETRA":"C"},
"INCUMPLIMIENTO ALIADO":{"LETRA":"I"},
"CAMARA/SOLDADA O INUNDADA":{"LETRA":"+"},
"FUERA DE COBERTURA WTTH":{"LETRA":"/"}
}


jsonRazonFields={
            "NO CONTACTO CON CLIENTE":[                
                {"TipoInput":"text","Nombre":"DATOS FACHADA"},
                {"TipoInput":"textarea","Nombre":"OBSERVACION"},
                ],
            "CLIENTE SOLICITA REPROGRAMAR":[
                {"TipoInput":"textarea","Nombre":"OBSERVACION"},
                ],
            "VENTA DEVUELTA AL ASESOR":[
                {"TipoInput":"text","Nombre":"SUPERVISOR"},
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"},
                ],
            "MAL AGENDADO/MAL PROGRAMADO":[
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"},
                ],
            "UNIDAD POSIBLE FRAUDE":[
                {"TipoInput":"text","Nombre":"SUPERVISOR"},
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"},
                ],
            "PERMISOS DE ADMINISTRACION":[
                {"TipoInput":"text","Nombre":"ATIENDE LLAMADA EN PORTERIA"},
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"},
                ],
            "NO INGRESO/CLIENTE CONFIRMA SERVICIO OK":[                
                {"TipoInput":"textarea","Nombre":"OBSERVACION"},
                ],
            "DUCTOS/INFRESTRUCTURA PREDIO NO APTA":[
                {"TipoInput":"text","Nombre":"SUPERVISOR"},
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"},
                ],
            "PROBLEMA ORDEN PUBLICO/ZONA ROJA":[
                {"TipoInput":"text","Nombre":"SUPERVISOR"},
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"},
                ],
            "SUSCRIPTOR NO ESTA EN CONDICIÓN DE ATENDER":[
                {"TipoInput":"text","Nombre":"ATIENDE LLAMADA"},
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"},
                ],
            "DIRECCION Y/O DATOS ERRADOS":[
                {"TipoInput":"text","Nombre":"SUPERVISOR "},
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"},
                ],
            "INCUMPLIMIENTO ALIADO":[
                    {"TipoInput":"text","Nombre":"SUPERVISOR "},
                    {"TipoInput":"textarea","Nombre":"OBSERVACIONES"},
                    ],
            "FALTA DE MATERIALES/EQUIPOS":[
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"},
                {"TipoInput":"select","Nombre":"MATERIAL","Opciones":["Cables","Mesh","Pasivos","STB","eMTA"]},
                ],
            "CLIENTE AUN NO DESEA EL TRABAJO":[
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"},
                ],
            "SUSCRIPTOR NO DESEA/NO REQUIERE TRABAJOS":[
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"},
                ],
            "CLIENTE NO TIENE DINERO":[
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"},
                ],
            "EQUIPOS CLIENTE NO APTOS/NO DISPONIBLES":[
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"},
                ],
            "LLUVIA - FACTORES CLIMÁTICOS":[
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"},
                ],
            "SEÑAL OK":[
                    {"TipoInput":"text","Nombre":"DATOS FACHADA"},
                    {"TipoInput":"textarea","Nombre":"OBSERVACION"},
                    ],
            "FUERA DE COBERTURA WTTH":[
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"},
                ],
            "PROBLEMAS EN SISTEMAS APLICATIVOS CLARO":[                
                {"TipoInput":"text","Nombre":"SUPERVISOR "},
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"},
                {"TipoInput":"text","Nombre":"RQ"},
                {"TipoInput":"select","Nombre":"APLICATIVO","Opciones":["ACS","GRF","MODULO DE GESTION","OFSC","RR"]},
                ],
            "INSTALACIÓN REQUIERE ANDAMIO ARNES":[
                {"TipoInput":"text","Nombre":"SUPERVISOR "},
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES "},
                ],
            "REPLANTEAMIENTO VT":[
                {"TipoInput":"text","Nombre":"ATIENDE LLAMADA"},
                {"TipoInput":"text","Nombre":"SUPERVISOR"},
                {"TipoInput":"text","Nombre":"SE REQUIERE ROMPER EN ZONA"},
                {"TipoInput":"text","Nombre":"METRAJE"},
                {"TipoInput":"text","Nombre":"SE REQUIERE DESTAPAR TUBERIA EXTERNA POR PARTE DE CLARO: SI/NO"},
                {"TipoInput":"text","Nombre":"TIEMPO PROMEDIO DE TRABAJO"},
                {"TipoInput":"text","Nombre":"MATERIAL REQUERIDO"},
                {"TipoInput":"text","Nombre":"SE REQUIERE MOVIL ELITE SI/NO"},
                {"TipoInput":"text","Nombre":"REGISTRAR NORMALIZACION"},
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"},
                ],
            "REQUIERE MOVIL ELITE":[
                {"TipoInput":"text","Nombre":"SUPERVISOR"},
                {"TipoInput":"text","Nombre":"SE REQUIERE ROMPER EN ZONA BLANDA O DURA"},
                {"TipoInput":"text","Nombre":"SE REQUIERE DESTAPAR TUBERIA EXTERNA POR PARTE DE CLARO: SI/NO"},
                {"TipoInput":"text","Nombre":"METRAJE"},
                {"TipoInput":"text","Nombre":"TIEMPO PROMEDIO DE TRABAJO"},
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"},
                ],
            "FUERA DE ZONA/SIN COBERTURA DE RED":[
                {"TipoInput":"text","Nombre":"SUPERVISOR" },
                {"TipoInput":"text","Nombre":"REGISTRAR NORMALIZACION"},
                {"TipoInput":"text","Nombre":"DISTANCIA PUNTO MAS CERCANO"},
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"}                
                ],
            "AMPLIACION DE TAP HFC":[
                {"TipoInput":"text","Nombre":"SUPERVISOR "},
                {"TipoInput":"text","Nombre":"DESCRIPCIÓN DE PUNTO DE REFERENCIA"},
                {"TipoInput":"text","Nombre":"DIRECCIÓN DE DISPOSITIVO ANTERIOR"},
                {"TipoInput":"text","Nombre":"VALOR DISPOSITIVO ANTERIOR"},
                {"TipoInput":"text","Nombre":"DIRECCIÓN DE DISPOSITIVO COPADO"},
                {"TipoInput":"text","Nombre":"VALOR DISPOSITIVO A COPADO"},
                {"TipoInput":"text","Nombre":"DIRECCIÓN DE DISPOSITIVO POSTERIOR"},
                {"TipoInput":"text","Nombre":"VALOR DISPOSITIVO POSTERIOR"},
                {"TipoInput":"text","Nombre":"NÚMERO DE POSTE"},
                {"TipoInput":"text","Nombre":"TIPO DE ACOMETIDA"},
                {"TipoInput":"text","Nombre":"REGISTRAR NORMALIZACION"},
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"},
                ],
                "AMPLIACION DE TAP FTTH":[
                    {"TipoInput":"text","Nombre":"SUPERVISOR "},
                    {"TipoInput":"text","Nombre":"DESCRIPCIÓN DE PUNTO DE REFERENCIA"},                    
                    {"TipoInput":"text","Nombre":"CANTIDAD DE DISPOSITIVO"},
                    {"TipoInput":"text","Nombre":"TIEMPO PROMEDIO A UTILIZAR"},
                    {"TipoInput":"text","Nombre":"MATERIALES A UTILIZAR"},
                    {"TipoInput":"text","Nombre":"REGISTRAR NORMALIZACION"},                    
                    {"TipoInput":"textarea","Nombre":"OBSERVACIONES"},
                    ],

            "PROBLEMAS EN LA RED EXTERNA":[
                {"TipoInput":"text","Nombre":"SUPERVISOR"},
                {"TipoInput":"text","Nombre":"NUM INC"},
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"}],
            
            
                "CAMARA/SOLDADA O INUNDADA":[
                {"TipoInput":"text","Nombre":"SUPERVISOR"},
                {"TipoInput":"text","Nombre":"NUM INC"},
                {"TipoInput":"textarea","Nombre":"OBSERVACIONES"}]
            

            }


'''for i in jsonRazonFields.keys():
	try:
		print(x[i])
	except Exception as e:
		print("=",e,i)
'''

jsonCauRazon = {"NO CONTACTO CON CLIENTE":["Cliente NO está en predio.",
            "El cliente NO fue notificar del agendamiento o la había solicitado para otro día.",
            "Cliente no sabe de la visita y no puede atender el servicio (SI SOLICITO LA VT)."],
            
            "CLIENTE SOLICITA REPROGRAMAR":["Técnico está realizado labores y el cliente ya no puede seguir atendiendo la visita.",
            "Técnico con cliente en predio y cliente solicite reagendar la visita."],
            
            "VENTA DEVUELTA AL ASESOR":["Cliente NO acepta costos de modificaciones en la orden.",
            "Cliente solamente hizo cotización del servicio, más no pidió el evento técnico.",
            "Cliente menciona que no le fue explicado los parámetros del servicio a realizar.",
            "Ofrecimientos del asesor comercial que por política no aplican (puntos nuevos o ya existentes en el predio.",
            "Cliente tiene dudas con el contrato comercial",
            "Requiere el servicio para una dirección diferente a la que inicialmente había solicitado.",
            "La orden esta digitada en un segmento que no corresponde."],
            
            "MAL AGENDADO/MAL PROGRAMADO":["Existen do o más OT/LLS creadas en la misma cuenta.",
            "Cliente no sabe del evento y tampoco lo solicito (NO TIENE CODIGO DE VENDEDOR).",
            "Nodo mal Georreferenciado. (CUANDO EL ALIADO NO PUEDA EJECUTAR LA VISITA).",
            "Cuando el cliente informa que el servicio es para otra cuenta (NO TIENE CODIGO DE VENDEDOR).",
            "Visita agendada en una carpeta diferente.",
            "Evento con datos errados, pero NO tiene código de vendedor."],
            
            "UNIDAD POSIBLE FRAUDE":["Ya hay servicios activos en la misma dirección.",
            "Predio tiene varios contadores y la instalación es en diferentes HHPP.",
            "Trabajos donde no hay muebles, ni personas establecidas, no conocen al suscriptor en el predio; pero solicitan un equipo."],
            
            "PERMISOS DE ADMINISTRACION":["NO hay acceso a cuartos de máquinas o NO esta la persona encargada que tenga las llaves para acceder a terrazas (todero).",
            "Cliente no pidió los permisos a la administración.",
            "Administración solicita carta con previa anticipación.",
            "NO hay permisos por parte del conjunto por daños causados por Claro."],
            
            "NO INGRESO/CLIENTE CONFIRMA SERVICIO OK":["El técnico NO ingresa al predio y le confirman que el servicio esta en funcionamiento.",
            "La LLS debe ser completada en sistema bajo el código S13."],
            
            "DUCTOS/INFRESTRUCTURA PREDIO NO APTA":["Ducteria interna saturada.",
            "Remodelaciones que demoren menos de 3 días, de lo contrario se aplica razón 7.",
            "Cliente no permite realizar perforaciones, cableado visible o reformas en la infraestructura.",
            "No hay fluido eléctrico en el predio."],
            
            "PROBLEMA ORDEN PUBLICO/ZONA ROJA":["Zona de alta inseguridad.",
            "Problemas de orden público, manifestaciones o marchas."],
            
            "SUSCRIPTOR NO ESTA EN CONDICIÓN DE ATENDER":["Cuando el cliente genere amenazas al personal técnico.",
            "Dueño no autoriza realizar el evento técnico.",
            "No hay acceso a cuartos de la vivienda (llaves o cielos rasos).",
            "Cuando atiende un menor de edad.",
            "Cliente esta no está en condiciones óptimos (ebriedad, alucinación, COVID)."],
            
            "DIRECCION Y/O DATOS ERRADOS":["Cualquier error que implique que la dirección este incorrecta (CODIGO DE VENDEDOR).",
            "Si la dirección no está creada en RR (aplica cancelación inmediata).",
            "Cuando el servicio va registrado como CASA y es para un edifico / cuenta matriz o viceversa."],
            
            "INCUMPLIMIENTO ALIADO":["Técnico no lleva materiales o herramientas. (escalera, arnés). No hay apoyo del aliado con dicho material.",
            "Técnico reporta razón falsa con incidentes o notas de lo sucedido en la visita.",
            "Técnico llega fuera de franja agendada.",
            "Si el técnico no realiza el evento o no responde el chat o llamadas.",
            "Técnico no lleva carnet, parafiscales, carta de responsabilidad de daños.",
            "NO aplica cuando la orden viene mal creada o el cliente no ha solicitado visita."],
            
            "FALTA DE MATERIALES/EQUIPOS":["NO hay existencias de equipos y/o abastecimiento de material en Bodega (Autorizado por Claro mediante correo).",
            "NO aplica para equipos básicos como escalera, andamios. Falta de otro tipo de material."],
            
            "CLIENTE AUN NO DESEA EL TRABAJO":["Cliente tiene servicios con otro operador que NO ha cancelado.",
            "Remodelaciones o adecuaciones en predio que superen los 3 días.",
            "Cliente si esta interesado en el servicio, pero aún no lo puede aceptar o no tiene fecha tentativa para reagendar el evento."],
            
            "SUSCRIPTOR NO DESEA/NO REQUIERE TRABAJOS":["Cliente de manera definitiva no requiere el servicio.",
            "Cliente ya servicio con otro operador y NO necesita gestión de Claro.",
            "Ya no necesitan el servicio por insatisfacción en los tiempos de respuesta."],
            
            "CLIENTE NO TIENE DINERO":["No cuenta con dinero para la instalación (aplica solo para DTH)"],
            
            "EQUIPOS CLIENTE NO APTOS/NO DISPONIBLES":["Cliente no tiene los equipos de Claro o los requeridos (TV, teléfono) para ejecutar los trabajos ",
            "Traslados donde exista pérdida o hurto de los equipos y aún se encuentren activos en el sistema.",
            "En postventas, cuando se requiere retirar o activar un decodificador que este en el inventario, pero físicamente no este el equipo en el predio.",
            "Cuando el cliente le hace falta algún equipo para ejecutar mantenimientos o postventas. ",
            "Si el cliente indica que NO tiene posibilidad de llevar o recuperar el equipo, debe ejecutar el tramite de liberación en un CAV."],
            
            "LLUVIA - FACTORES CLIMÁTICOS":["Que se encuentre lloviendo y que sea confirmado por el cliente.  ",
            "Techo o dispositivos húmedos o mojados. ",
            "No hay lluvia, pero si riesgo de tormenta eléctrica o relámpagos.",
            "Solamente aplica para trabajos externos (TAP, NAP, techos. CAJA RELIANCE NO APLICA)."],
            
            "SEÑAL OK":["El técnico NO ingresa al predio y le confirman que el servicio esta en funcionamiento.",
            "La LLS debe ser completada en sistema bajo el código S13."],
            
            "FUERA DE COBERTURA WTTH":["Cuando no hay red Bidireccional y FTTH en la zona.",
            "Si hay acometida de servicio eléctrico, pero no pasa red externa en donde se va a dar la señal al HHPP."],
            
            "PROBLEMAS EN SISTEMAS APLICATIVOS CLARO":["Inconvenientes masivos con la plataforma de Módulo de Gestión, RR, ACS, GRF, WFM.",
            "Siempre incluir el número de Ticket o REQ."],
            
            "INSTALACIÓN REQUIERE ANDAMIO ARNES":["Cuando es necesario usar andamios o descolgadas para ejecutar la instalación.",
            "Se requiere permisos de ascensores y no se ha realizado ese proceso."],
            
            "REPLANTEAMIENTO VT":["Cuando la acometida para por empresas que presten servicio eléctrico.",
            "Ducteria externa saturada validada con el supervisor o interventor,",
            "Si la matriz NO tiene acometida o eta de manera parcial para llevar señal al HHPP.",
            "Si la matriz NO tiene visita técnica o la requiere para cada instalación.",
            "Cuando hay andenes del IDU y se requiere acondicionamiento.",
            "Cuando la cámara corresponde a otro operador.",
            "Administración solicita reubicación de cajas.",
            "No se halla dispositivo en la parte externa.",
            "Aquí se debe confirmar si se debe romper zona dura o zona blanda y cuantos metros; si son o no andenes del IDU; que tipo de material se requiere para realizar el acondicionamiento."],
            
            "REQUIERE MOVIL ELITE":["Cuando la Ducteria externa este saturada y el supervisor confirme que requiera móvil elite; de lo contrario debe quedar con R.",
            "Adecuaciones máximo de 10 metros de zona dura y 15 metros de zona blanda."],
            "FUERA DE ZONA/SIN COBERTURA DE RED":["Cuando no hay red Bidireccional y FTTH en la zona.",
            "Si hay acometida de servicio eléctrico, pero no pasa red externa en donde se va a dar la señal al HHPP."],
            
            "AMPLIACION DE TAP HFC":["Dispositivo o puerto copado (Caja, cámara, poste).",
            "En LLS cuando el cliente fue desconectado y los puertos están ocupados.",
            "Esta razón debe ser confirmada tanto con el cliente como con el supervisor, adicional, debe ir registrada la normalización para confirmar los puertos copados."],
            "AMPLIACION DE TAP FTTH":["Dispositivo o puerto copado (Caja, cámara, poste)",
            "En LLS cuando el cliente fue desconectado y los puertos están ocupados.",
            "Esta razón debe ser confirmada tanto con el cliente como con el supervisor, adicional, debe ir registrada la normalización para confirmar los puertos copados."],
            "PROBLEMAS EN LA RED EXTERNA":["Fallas externas que afectan a varios clientes esta gestion es del area de CSI"],
            "CAMARA/SOLDADA O INUNDADA":["Se requiere abrir la camara pero esta inundada o soldada, esta gestion es del area de CSI"]
            }
'''
for i in x.keys():
	try:
		x[i]["CausaRazon"]=jsonCauRazon[i]
	except Exception as e:
		print(e,i)

for i,j in x.items():
	print('"%s":'%i,j,",")
	#break'''

'''ax=list(x.keys())
print(ax)

ai=list(jsonRazonFields.keys())
print(ai)

for i in ai:
	print(i in ax,i)'''


dx={'AMPLIACION DE TAP HFC': {'LETRA': 'H', 'AtributoHtml': [{'TipoInput': 'text', 'Nombre': 'SUPERVISOR '}, {'TipoInput': 'text', 'Nombre': 'DESCRIPCIÓN DE PUNTO DE REFERENCIA'}, {'TipoInput': 'text', 'Nombre': 'DIRECCIÓN DE DISPOSITIVO ANTERIOR'}, {'TipoInput': 'text', 'Nombre': 'VALOR DISPOSITIVO ANTERIOR'}, {'TipoInput': 'text', 'Nombre': 'DIRECCIÓN DE DISPOSITIVO COPADO'}, {'TipoInput': 'text', 'Nombre': 'VALOR DISPOSITIVO A COPADO'}, {'TipoInput': 'text', 'Nombre': 'DIRECCIÓN DE DISPOSITIVO POSTERIOR'}, {'TipoInput': 'text', 'Nombre': 'VALOR DISPOSITIVO POSTERIOR'}, {'TipoInput': 'text', 'Nombre': 'NÚMERO DE POSTE'}, {'TipoInput': 'text', 'Nombre': 'TIPO DE ACOMETIDA'}, {'TipoInput': 'text', 'Nombre': 'REGISTRAR NORMALIZACION'}, {'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': ['Dispositivo o puerto copado (Caja, cámara, poste).', 'En LLS cuando el cliente fue desconectado y los puertos están ocupados.', 'Esta razón debe ser confirmada tanto con el cliente como con el supervisor, adicional, debe ir registrada la normalización para confirmar los puertos copados.']}, 'AMPLIACION DE TAP FTTH': {'LETRA': 'H', 'AtributoHtml': [{'TipoInput': 'text', 'Nombre': 'SUPERVISOR '}, {'TipoInput': 'text', 'Nombre': 'DESCRIPCIÓN DE PUNTO DE REFERENCIA'}, {'TipoInput': 'text', 'Nombre': 'CANTIDAD DE DISPOSITIVO'}, {'TipoInput': 'text', 'Nombre': 'TIEMPO PROMEDIO A UTILIZAR'}, {'TipoInput': 'text', 'Nombre': 'MATERIALES A UTILIZAR'}, {'TipoInput': 'text', 'Nombre': 'REGISTRAR NORMALIZACION'}, {'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': ['Dispositivo o puerto copado (Caja, cámara, poste)', 'En LLS cuando el cliente fue desconectado y los puertos están ocupados.', 'Esta razón debe ser confirmada tanto con el cliente como con el supervisor, adicional, debe ir registrada la normalización para confirmar los puertos copados.']}, 'CLIENTE AUN NO DESEA EL TRABAJO': {'LETRA': '7', 'AtributoHtml': [{'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': ['Cliente tiene servicios con otro operador que NO \
ha cancelado.', 'Remodelaciones o adecuaciones en predio que superen los 3 días.', 'Cliente si esta interesado en el servicio, pero aún no lo puede \
aceptar o no tiene fecha tentativa para reagendar el evento.']}, 'CLIENTE NO TIENE DINERO': {'LETRA': 'O', 'AtributoHtml': [{'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': ['No cuenta con dinero para la instalación (aplica solo para DTH)']}, 'CLIENTE SOLICITA REPROGRAMAR': {'LETRA': 'K', 'AtributoHtml': [{'TipoInput': 'textarea', 'Nombre': 'OBSERVACION'}], 'CausaRazon': ['Técnico está realizado labores y el cliente ya no puede seguir atendiendo la visita.', 'Técnico con cliente en predio y cliente solicite reagendar la visita.']}, 'DIRECCION Y/O DATOS ERRADOS': {'LETRA': 'B', 'AtributoHtml': [{'TipoInput': 'text', 'Nombre': 'SUPERVISOR '}, {'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': ['Cualquier error que implique que la dirección este incorrecta (CODIGO DE VENDEDOR).', 'Si la dirección no está creada en RR (aplica cancelación inmediata).', 'Cuando el servicio va registrado como CASA y es para un edifico / cuenta matriz o viceversa.']}, 'DUCTOS/INFRESTRUCTURA PREDIO NO APTA': \
{'LETRA': 'W', 'AtributoHtml': [{'TipoInput': 'text', 'Nombre': 'SUPERVISOR'}, {'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': \
['Ducteria interna saturada.', 'Remodelaciones que demoren menos de 3 días, de lo contrario se aplica razón 7.', 'Cliente no permite realizar perforaciones, cableado visible o reformas en la infraestructura.', 'No hay fluido eléctrico en el predio.']}, 'EQUIPOS CLIENTE NO APTOS/NO DISPONIBLES': \
{'LETRA': '6', 'AtributoHtml': [{'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': ['Cliente no tiene los equipos de Claro o los requeridos (TV, teléfono) para ejecutar los trabajos ', 'Traslados donde exista pérdida o hurto de los equipos y aún se encuentren activos en el sistema.', 'En postventas, cuando se requiere retirar o activar un decodificador que este en el inventario, pero físicamente no este el equipo en el predio.', 'Cuando el cliente le hace falta algún equipo para ejecutar mantenimientos o postventas. ', 'Si el cliente indica que NO tiene posibilidad de llevar o recuperar el equipo, debe ejecutar el tramite de liberación en un CAV.']}, 'FALTA DE MATERIALES/EQUIPOS': {'LETRA': 'F', 'AtributoHtml': [{'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}, {'TipoInput': 'select', 'Nombre': 'MATERIAL', 'Opciones': ['Cables', 'Mesh', 'Pasivos', 'STB', 'eMTA']}], 'CausaRazon': ['NO hay existencias de equipos y/o abastecimiento de material en Bodega (Autorizado por Claro mediante correo).', 'NO aplica para equipos básicos como escalera, andamios. Falta de otro tipo de material.']}, 'FUERA DE ZONA/SIN COBERTURA DE RED': {'LETRA': 'Z', 'AtributoHtml': [{'TipoInput': 'text', 'Nombre': 'SUPERVISOR'}, {'TipoInput': 'text', 'Nombre': 'REGISTRAR NORMALIZACION'}, {'TipoInput': 'text', 'Nombre': 'DISTANCIA PUNTO MAS CERCANO'}, {'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': ['Cuando no hay red Bidireccional y FTTH en la zona.', 'Si hay acometida de servicio eléctrico, pero no pasa red externa en donde se va a dar la señal al HHPP.']}, 'INSTALACIÓN REQUIERE ANDAMIO ARNES': {'LETRA': 'Y', 'AtributoHtml': [{'TipoInput': 'text', 'Nombre': 'SUPERVISOR '}, {'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES '}], 'CausaRazon': ['Cuando es necesario usar andamios o descolgadas para ejecutar la instalación.', 'Se requiere permisos de ascensores y no se ha realizado ese proceso.']}, 'LLUVIA - FACTORES CLIMÁTICOS': {'LETRA': 'L', 'AtributoHtml': [{'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': ['Que se encuentre lloviendo y que sea confirmado por el cliente.  ', 'Techo o dispositivos húmedos o mojados. ', 'No hay lluvia, pero si riesgo de tormenta eléctrica o relámpagos.', 'Solamente aplica para trabajos externos (TAP, NAP, techos. CAJA RELIANCE NO APLICA).']}, 'MAL AGENDADO/MAL PROGRAMADO': {'LETRA': 'M', 'AtributoHtml': [{'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': ['Existen do o más OT/LLS creadas en la misma cuenta.', 'Cliente no sabe del evento y tampoco lo solicito (NO TIENE CODIGO DE VENDEDOR).', 'Nodo mal Georreferenciado. (CUANDO EL ALIADO NO PUEDA EJECUTAR LA VISITA).', 'Cuando el cliente informa que el servicio es para otra cuenta (NO TIENE CODIGO DE VENDEDOR).', 'Visita agendada en una carpeta diferente.', 'Evento con datos errados, pero NO tiene código de vendedor.']}, 'NO INGRESO/CLIENTE CONFIRMA SERVICIO OK': {'LETRA': 'S', 'AtributoHtml': [{'TipoInput': 'textarea', 'Nombre': 'OBSERVACION'}], 'CausaRazon': ['El técnico NO ingresa al predio y le confirman que el servicio \
esta en funcionamiento.', 'La LLS debe ser completada en sistema bajo el código S13.']}, 'PERMISOS DE ADMINISTRACION': {'LETRA': 'P', 'AtributoHtml': [{'TipoInput': 'text', 'Nombre': 'ATIENDE LLAMADA EN PORTERIA'}, {'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': ['NO hay acceso a cuartos de máquinas o NO esta la persona encargada que tenga las llaves para acceder a terrazas (todero).', 'Cliente no pidió los permisos a la administración.', 'Administración solicita carta con previa anticipación.', 'NO hay permisos por parte del conjunto por daños causados por Claro.']}, 'PROBLEMA ORDEN PUBLICO/ZONA ROJA': {'LETRA': 'X', 'AtributoHtml': [{'TipoInput': 'text', 'Nombre': 'SUPERVISOR'}, {'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': ['Zona de alta inseguridad.', 'Problemas de orden público, manifestaciones o marchas.']}, 'PROBLEMAS EN LA RED EXTERNA': {'LETRA': '%', 'AtributoHtml': [{'TipoInput': 'text', 'Nombre': 'SUPERVISOR'}, {'TipoInput': 'text', 'Nombre': 'NUM INC'}, {'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': ['Fallas externas que afectan a varios clientes esta gestion es del area de CSI']}, 'PROBLEMAS EN SISTEMAS APLICATIVOS CLARO': {'LETRA': 'Q', 'AtributoHtml': [{'TipoInput': 'text', 'Nombre': 'SUPERVISOR '}, {'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}, {'TipoInput': 'text', 'Nombre': 'RQ'}, {'TipoInput': 'select', 'Nombre': 'APLICATIVO', 'Opciones': ['ACS', 'GRF', 'MODULO DE GESTION', 'OFSC', 'RR']}], 'CausaRazon': ['Inconvenientes masivos con la plataforma de Módulo de Gestión, RR, ACS, GRF, WFM.', 'Siempre incluir el número de Ticket o REQ.']}, 'REPLANTEAMIENTO VT': {'LETRA': 'R', 'AtributoHtml': [{'TipoInput': 'text', 'Nombre': 'ATIENDE LLAMADA'}, {'TipoInput': 'text', 'Nombre': 'SUPERVISOR'}, {'TipoInput': 'text', 'Nombre': 'SE REQUIERE ROMPER EN ZONA'}, {'TipoInput': 'text', 'Nombre': 'METRAJE'}, {'TipoInput': 'text', 'Nombre': 'SE REQUIERE DESTAPAR TUBERIA EXTERNA POR PARTE DE CLARO: SI/NO'}, {'TipoInput': 'text', 'Nombre': 'TIEMPO PROMEDIO DE TRABAJO'}, {'TipoInput': 'text', 'Nombre': 'MATERIAL REQUERIDO'}, {'TipoInput': 'text', 'Nombre': 'SE REQUIERE MOVIL ELITE SI/NO'}, {'TipoInput': 'text', 'Nombre': 'REGISTRAR NORMALIZACION'}, {'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': ['Cuando la acometida para por empresas que presten servicio eléctrico.', 'Ducteria externa saturada validada con el supervisor o interventor,', 'Si la matriz NO tiene acometida o eta de manera parcial para llevar señal al HHPP.', 'Si la matriz NO tiene visita técnica o la requiere para cada instalación.', 'Cuando hay andenes del IDU y \
se requiere acondicionamiento.', 'Cuando la cámara corresponde a otro operador.', 'Administración solicita reubicación de cajas.', 'No se halla dispositivo en la parte externa.', 'Aquí se debe confirmar si se debe romper zona dura o zona blanda y cuantos metros; si son o no andenes del IDU; que \
tipo de material se requiere para realizar el acondicionamiento.']}, 'REQUIERE MOVIL ELITE': {'LETRA': '=', 'AtributoHtml': [{'TipoInput': 'text', 'Nombre': 'SUPERVISOR'}, {'TipoInput': 'text', 'Nombre': 'SE REQUIERE ROMPER EN ZONA BLANDA O DURA'}, {'TipoInput': 'text', 'Nombre': 'SE REQUIERE DESTAPAR TUBERIA EXTERNA POR PARTE DE CLARO: SI/NO'}, {'TipoInput': 'text', 'Nombre': 'METRAJE'}, {'TipoInput': 'text', 'Nombre': 'TIEMPO PROMEDIO DE \
TRABAJO'}, {'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': ['Cuando la Ducteria externa este saturada y el supervisor confirme \
que requiera móvil elite; de lo contrario debe quedar con R.', 'Adecuaciones máximo de 10 metros de zona dura y 15 metros de zona blanda.']}, 'SUSCRIPTOR NO DESEA/NO REQUIERE TRABAJOS': {'LETRA': 'E', 'AtributoHtml': [{'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': ['Cliente de manera definitiva no requiere el servicio.', 'Cliente ya servicio con otro operador y NO necesita gestión de Claro.', 'Ya no necesitan el servicio por insatisfacción en los tiempos de respuesta.']}, 'SUSCRIPTOR NO ESTA EN CONDICIÓN DE ATENDER': {'LETRA': '?', 'AtributoHtml': [{'TipoInput': 'text', 'Nombre': 'ATIENDE LLAMADA'}, {'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': ['Cuando el cliente genere amenazas al personal técnico.', 'Dueño no autoriza realizar el evento técnico.', 'No hay acceso a cuartos de la vivienda (llaves o cielos rasos).', 'Cuando atiende un menor de edad.', 'Cliente esta no está en condiciones óptimos (ebriedad, alucinación, COVID).']}, 'UNIDAD POSIBLE FRAUDE': {'LETRA': 'V', 'AtributoHtml': [{'TipoInput': 'text', 'Nombre': 'SUPERVISOR'}, {'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': ['Ya hay servicios activos en la misma dirección.', 'Predio tiene varios contadores y la instalación es en diferentes HHPP.', 'Trabajos donde no hay muebles, ni personas establecidas, no conocen al suscriptor en el predio; pero solicitan un equipo.']}, 'VENTA DEVUELTA AL ASESOR': {'LETRA': '4', 'AtributoHtml': [{'TipoInput': 'text', 'Nombre': 'SUPERVISOR'}, {'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': ['Cliente NO acepta costos de modificaciones en la orden.', 'Cliente solamente hizo cotización del servicio, más no pidió el evento técnico.', 'Cliente menciona que no le fue explicado los parámetros del servicio a realizar.', 'Ofrecimientos del asesor comercial que por política no aplican (puntos nuevos o ya existentes en el predio.', 'Cliente tiene dudas con el contrato comercial', 'Requiere el servicio para una dirección diferente a la que inicialmente había solicitado.', \
'La orden esta digitada en un segmento que no corresponde.']}, 'NO CONTACTO CON CLIENTE': {'LETRA': 'C', 'AtributoHtml': [{'TipoInput': 'text', 'Nombre': 'DATOS FACHADA'}, {'TipoInput': 'textarea', 'Nombre': 'OBSERVACION'}], 'CausaRazon': ['Cliente NO está en predio.', 'El cliente NO fue notificar del agendamiento o la había solicitado para otro día.', 'Cliente no sabe de la visita y no puede atender el servicio (SI SOLICITO LA VT).']}, 'INCUMPLIMIENTO ALIADO': {'LETRA': 'I', 'AtributoHtml': [{'TipoInput': 'text', 'Nombre': 'SUPERVISOR '}, {'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': ['Técnico no lleva materiales o herramientas. (escalera, arnés). No hay apoyo del aliado con dicho material.', 'Técnico reporta razón falsa con incidentes o notas de lo sucedido en la visita.', 'Técnico llega fuera de franja agendada.', 'Si el técnico no realiza el evento \
o no responde el chat o llamadas.', 'Técnico no lleva carnet, parafiscales, carta de responsabilidad de daños.', 'NO aplica cuando la orden viene mal creada o el cliente no ha solicitado visita.']}, 'CAMARA/SOLDADA O INUNDADA': {'LETRA': '+', 'AtributoHtml': [{'TipoInput': 'text', 'Nombre': 'SUPERVISOR'}, {'TipoInput': 'text', 'Nombre': 'NUM INC'}, {'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': ['Se requiere abrir la camara pero esta inundada o soldada, esta gestion es del area de CSI']}, 'FUERA DE COBERTURA WTTH': {'LETRA': '/', 'AtributoHtml': [{'TipoInput': 'textarea', 'Nombre': 'OBSERVACIONES'}], 'CausaRazon': ['Cuando no hay red Bidireccional y FTTH en la zona.', 'Si hay acometida de servicio eléctrico, \
pero no pasa red externa en donde se va a dar la señal al HHPP.']}}




for i,j in dx.items():
	print(j['AtributoHtml'])
	break
# Turing_Machine

# 🧠 Máquina de Turing en Python | Explicación paso a paso

Este proyecto implementa una **Máquina de Turing** en **Python**, simulando cómo este modelo teórico de la computación procesa información a través de una cinta infinita.  
Fue creado con fines educativos para comprender el funcionamiento interno de un algoritmo de forma visual y sencilla.

---

## 🎯 Objetivo

Simular una **Máquina de Turing** capaz de **escribir el nombre “MATEO”** en una cinta vacía, siguiendo reglas simples de lectura, escritura y movimiento del cabezal.

---

## 🧩 Concepto teórico

Una **Máquina de Turing** es un modelo matemático propuesto por **Alan Turing** en 1936.  
Se compone de:

- Una **cinta infinita** dividida en celdas.
- Un **cabezal** que lee y escribe símbolos.
- Un **conjunto de estados** (q0, q1, q2, …).
- Una **tabla de transiciones** que define qué hacer en cada paso.
- Un **estado de parada (HALT)**.

El funcionamiento general es:

> “Si estoy en cierto estado y leo un símbolo, escribo algo, me muevo y cambio de estado.”

Este principio es la base de **toda computadora moderna**.

---

## 💻 Código principal (`main.py`)

El script define:

- La clase `Transition`: describe qué escribir, hacia dónde moverse y a qué estado ir.
- La clase `TuringMachine`: controla el estado, la cinta y el cabezal.
- Una lista de reglas que permiten escribir el nombre **MATEO** paso a paso.

Cada transición sigue el formato:

```python
(state, read_symbol) -> (write_symbol, move_direction, next_state)

📘 Referencias

Alan Turing, On Computable Numbers, with an Application to the Entscheidungsproblem (1936)
Wikipedia: Máquina de Turing
Python Documentation: Dataclasses

Autor: Mateo Henao Correa
Estudiante de Ingeniería de Software 🎓
Universidad Iberoamericana

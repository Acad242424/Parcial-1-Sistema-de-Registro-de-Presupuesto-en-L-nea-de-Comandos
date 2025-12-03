#!/usr/bin/env python3
"""
Budget CLI - app.py
Simple command-line application to manage budget items using SQLite.
Usage:
    python app.py            # interactive menu
    python app.py --help     # show help
"""

import sqlite3
import sys
from storage import Storage
from tabulate import tabulate

DB_PATH = "budget.db"

def input_nonempty(prompt):
    while True:
        v = input(prompt).strip()
        if v:
            return v
        print("Entrada vacía. Por favor ingresa un valor.")

def input_int(prompt):
    while True:
        try:
            return int(input_nonempty(prompt))
        except ValueError:
            print("Por favor ingresa un número entero válido.")

def input_float(prompt):
    while True:
        try:
            return float(input_nonempty(prompt))
        except ValueError:
            print("Por favor ingresa un número (decimal) válido.")

def show_item(item):
    keys = ["id","name","category","quantity","unit_price","description","created_at","updated_at"]
    for k,v in zip(keys, item):
        print(f"{k}: {v}")

def list_items(storage):
    items = storage.list_all()
    if not items:
        print("No hay artículos registrados.")
        return
    headers = ["ID","Nombre","Categoría","Cantidad","Precio Unit.","Descripción"]
    rows = [(i[0], i[1], i[2], i[3], f"{i[4]:.2f}", (i[5] or "")[:40]) for i in items]
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def register_item(storage):
    print("Registrar nuevo artículo")
    name = input_nonempty("Nombre: ")
    category = input_nonempty("Categoría: ")
    quantity = input_int("Cantidad: ")
    unit_price = input_float("Precio unitario: ")
    description = input("Descripción (opcional): ").strip()
    item_id = storage.create(name, category, quantity, unit_price, description)
    print(f"Artículo creado con ID {item_id}.")

def search_items(storage):
    print("Buscar artículos")
    q = input_nonempty("Buscar por nombre o categoría: ")
    results = storage.search(q)
    if not results:
        print("No se encontraron artículos.")
        return
    headers = ["ID","Nombre","Categoría","Cantidad","Precio Unit.","Descripción"]
    rows = [(i[0], i[1], i[2], i[3], f"{i[4]:.2f}", (i[5] or "")[:40]) for i in results]
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def edit_item(storage):
    print("Editar artículo")
    ident = input_nonempty("Ingresa ID del artículo a editar: ")
    try:
        ident = int(ident)
    except ValueError:
        print("ID inválido.")
        return
    item = storage.get_by_id(ident)
    if not item:
        print("Artículo no encontrado.")
        return
    print("Valores actuales:")
    show_item(item)
    print("Deja en blanco para mantener el valor actual.")
    name = input(f"Nombre [{item[1]}]: ").strip() or item[1]
    category = input(f"Categoría [{item[2]}]: ").strip() or item[2]
    qty_raw = input(f"Cantidad [{item[3]}]: ").strip()
    quantity = item[3]
    if qty_raw:
        try:
            quantity = int(qty_raw)
        except ValueError:
            print("Cantidad inválida. Se mantiene el valor actual.")
    price_raw = input(f"Precio unitario [{item[4]}]: ").strip()
    unit_price = item[4]
    if price_raw:
        try:
            unit_price = float(price_raw)
        except ValueError:
            print("Precio inválido. Se mantiene el valor actual.")
    description = input(f"Descripción [{item[5] or ''}]: ").strip() or item[5]
    storage.update(ident, name, category, quantity, unit_price, description)
    print("Artículo actualizado.")

def delete_item(storage):
    print("Eliminar artículo")
    ident = input_nonempty("Ingresa ID del artículo a eliminar: ")
    try:
        ident = int(ident)
    except ValueError:
        print("ID inválido.")
        return
    item = storage.get_by_id(ident)
    if not item:
        print("Artículo no encontrado.")
        return
    confirm = input(f"¿Confirmas eliminar '{item[1]}'? (s/N): ").strip().lower()
    if confirm == "s":
        storage.delete(ident)
        print("Artículo eliminado.")
    else:
        print("Operación cancelada.")

def main_menu():
    storage = Storage(DB_PATH)
    storage.ensure_tables()
    actions = {
        "1": ("Listar artículos", list_items),
        "2": ("Registrar artículo", register_item),
        "3": ("Buscar artículos", search_items),
        "4": ("Editar artículo", edit_item),
        "5": ("Eliminar artículo", delete_item),
        "0": ("Salir", None),
    }
    while True:
        print("\n--- Menú Principal ---")
        for k,(txt,_) in actions.items():
            print(f"{k}. {txt}")
        choice = input("Selecciona una opción: ").strip()
        if choice == "0":
            print("Hasta luego.")
            break
        action = actions.get(choice)
        if not action:
            print("Opción inválida.")
            continue
        action[1](storage)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario. Saliendo...")

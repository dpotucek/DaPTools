#!/usr/bin/env python3
"""
Alkoholové výpočty - Dilution a Mixing
===========================================================
Created by David Potucek on 4/15/26
Project: DaPTools
File: redeni.py

Skript pro výpočet ředění a míchání alkoholových roztoků.
Podporuje CLI parametry i interaktivní režim.
"""

import argparse
import sys


def dilution(v_start: float, c_poc: float, c_cil: float) -> float:
    """
    Vypočítá objem vody, který je třeba přidat k existujícímu objemu alkoholu.
    """
    if v_start <= 0:
        raise ValueError("Počáteční objem musí být kladné číslo")
    if c_poc <= 0 or c_poc > 100:
        raise ValueError("Počáteční koncentrace musí být mezi 0 a 100 %")
    if c_cil <= 0 or c_cil > 100:
        raise ValueError("Cílová koncentrace musí být mezi 0 a 100 %")
    if c_cil >= c_poc:
        raise ValueError("Cílová koncentrace musí být nižší než počáteční")

    return v_start * (c_poc / c_cil - 1)


def mixing(v_cil: float, c_poc: float, c_cil: float) -> tuple:
    """
    Vypočítá potřebný objem silného alkoholu a vody pro přípravu cílového roztoku.
    """
    if v_cil <= 0:
        raise ValueError("Cílový objem musí být kladné číslo")
    if c_poc <= 0 or c_poc > 100:
        raise ValueError("Počáteční koncentrace musí být mezi 0 a 100 %")
    if c_cil <= 0 or c_cil > 100:
        raise ValueError("Cílová koncentrace musí být mezi 0 a 100 %")
    if c_cil > c_poc:
        raise ValueError("Cílová koncentrace nemůže být vyšší než počáteční")

    v_alkohol = v_cil * (c_cil / c_poc)
    v_voda = v_cil - v_alkohol
    return v_alkohol, v_voda


def print_dilution_result(v_start: float, c_poc: float, c_cil: float, v_voda: float) -> None:
    print("\n" + "=" * 60)
    print("VÝSLEDEK: ŘEDĚNÍ (DILUTION)")
    print("=" * 60)
    print(f"\nPůvodní stav:")
    print(f"  Objem alkoholu:     {v_start:.3f} litrů")
    print(f"  Koncentrace:        {c_poc:.1f} %")
    print(f"\nCílová koncentrace: {c_cil:.1f} %")
    print(f"\nPotřebné množství vody k přidání: {v_voda:.3f} litrů ({v_voda * 1000:.1f} ml)")
    print(f"\nCelkový konečný objem: {v_start + v_voda:.3f} litrů")
    print("=" * 60)


def print_mixing_result(v_cil: float, c_poc: float, c_cil: float,
                        v_alkohol: float, v_voda: float) -> None:
    print("\n" + "=" * 60)
    print("VÝSLEDEK: SMÍCHÁVÁNÍ (MIXING)")
    print("=" * 60)
    print(f"\nCílový stav:")
    print(f"  Celkový objem:      {v_cil:.3f} litrů")
    print(f"  Cílová koncentrace: {c_cil:.1f} %")
    print(f"\nPotřebné složky:")
    print(f"  Alkohol ({c_poc:.1f}%):  {v_alkohol:.3f} litrů ({v_alkohol * 1000:.1f} ml)")
    print(f"  Voda (0%):           {v_voda:.3f} litrů ({v_voda * 1000:.1f} ml)")
    print(f"\nOvěření: {v_alkohol + v_voda:.3f} litrů (celkový objem)")
    print("=" * 60)


def get_float_input(prompt: str) -> float:
    """Získá float vstup s validací."""
    while True:
        try:
            val = input(prompt).strip()
            if val.lower() in ['q', 'quit', 'exit']:
                return None
            return float(val)
        except ValueError:
            print("  ❌ Neplatný vstup. Zadej číslo nebo 'q' pro ukončení.")


def interactive_mode():
    """Spustí interaktivní režim."""
    print("\n" + "=" * 60)
    print("INTERAKTIVNÍ REŽIM - Výpočet alkoholových roztoků")
    print("=" * 60)
    print("Zadej 'q' v jakémkoli kroku pro ukončení programu.")
    print("Tip: Pro výstup z interaktivního režimu zadej 'q' při výběru typu.")
    print("-" * 60)

    while True:
        print("\nVyberte typ výpočtu:")
        print("  1. Ředění (Dilution) - Přidání vody k existujícímu alkoholu")
        print("  2. Smíchávání (Mixing) - Příprava roztoku z alkoholu a vody")
        print("  q. Ukončit program")

        choice = input("\nVaše volba [1/2/q]: ").strip().lower()

        if choice == 'q':
            print("\nDěkuji za použití kalkulačky. Ahoj!")
            break

        if choice not in ['1', '2']:
            print("❌ Neplatná volba. Zkus to znovu.")
            continue

        try:
            if choice == '1':
                # Scénář: Ředění
                print("\n--- ŘEDĚNÍ ---")
                v_start = get_float_input("Zadej počáteční objem alkoholu (l): ")
                if v_start is None: continue

                c_poc = get_float_input("Zadej počáteční koncentraci (%): ")
                if c_poc is None: continue

                c_cil = get_float_input("Zadej cílovou koncentraci (%): ")
                if c_cil is None: continue

                v_voda = dilution(v_start, c_poc, c_cil)
                print_dilution_result(v_start, c_poc, c_cil, v_voda)

            elif choice == '2':
                # Scénář: Smíchávání
                print("\n--- SMÍCHÁVÁNÍ ---")
                v_cil = get_float_input("Zadej požadovaný celkový objem (l): ")
                if v_cil is None: continue

                c_poc = get_float_input("Zadej koncentraci dostupného alkoholu (%): ")
                if c_poc is None: continue

                c_cil = get_float_input("Zadej požadovanou cílovou koncentraci (%): ")
                if c_cil is None: continue

                v_alkohol, v_voda = mixing(v_cil, c_poc, c_cil)
                print_mixing_result(v_cil, c_poc, c_cil, v_alkohol, v_voda)

        except ValueError as e:
            print(f"\n❌ Chyba ve výpočtu: {e}")

        # Otázka na opakování
        again = input("\nChceš provést další výpočet? (ano/ne): ").strip().lower()
        if again not in ['ano', 'a', 'yes', 'y']:
            print("\nDěkuji za použití kalkulačky. Ahoj!")
            break


def main():
    parser = argparse.ArgumentParser(
        description="Výpočet ředění a míchání alkoholových roztoků",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Příklady použití:
  %(prog)s dilution --v-start 1 --c-poc 74 --c-cil 40
  %(prog)s mixing --v-cil 10 --c-poc 74 --c-cil 40
  %(prog)s --interactive  (nebo bez parametrů)
        """
    )

    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Spustit interaktivní režim')

    subparsers = parser.add_subparsers(dest='command', help='Typ výpočtu')

    # Subparser pro dilution
    dil_parser = subparsers.add_parser('dilution', help='Výpočet ředění (přidání vody)')
    dil_parser.add_argument('--v-start', type=float, required=True,
                            help='Počáteční objem alkoholu (litry)')
    dil_parser.add_argument('--c-poc', type=float, required=True,
                            help='Počáteční koncentrace (%)')
    dil_parser.add_argument('--c-cil', type=float, required=True,
                            help='Cílová koncentrace (%)')

    # Subparser pro mixing
    mix_parser = subparsers.add_parser('mixing', help='Výpočet smíchávání (příprava z komponent)')
    mix_parser.add_argument('--v-cil', type=float, required=True,
                            help='Cílový celkový objem (litry)')
    mix_parser.add_argument('--c-poc', type=float, required=True,
                            help='Koncentrace dostupného alkoholu (%)')
    mix_parser.add_argument('--c-cil', type=float, required=True,
                            help='Cílová koncentrace (%)')

    args = parser.parse_args()

    # Logika spuštění
    if args.interactive or (not args.command and not args.interactive):
        # Pokud je flag --interactive nebo žádné argumenty -> interaktivní režim
        interactive_mode()
        return

    try:
        if args.command == 'dilution':
            v_voda = dilution(args.v_start, args.c_poc, args.c_cil)
            print_dilution_result(args.v_start, args.c_poc, args.c_cil, v_voda)

        elif args.command == 'mixing':
            v_alkohol, v_voda = mixing(args.v_cil, args.c_poc, args.c_cil)
            print_mixing_result(args.v_cil, args.c_poc, args.c_cil, v_alkohol, v_voda)

    except ValueError as e:
        print(f"\nChyba: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
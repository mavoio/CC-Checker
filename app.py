import re
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.layout import Layout
from rich.live import Live
from rich.align import Align
from rich.style import Style
from rich.text import Text
from colorama import init
import pyfiglet
from datetime import datetime
from art import text2art
import time
import json

# Initialize colorama
init()

console = Console()

def get_bin_info(card_number):
    """Get detailed BIN information for the card"""
    try:
        bin_number = str(card_number)[:6]
        response = requests.get(f"https://lookup.binlist.net/{bin_number}", timeout=4)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def luhn_algorithm(card_number):
    """Implementation of Luhn's algorithm for card validation"""
    digits = [int(d) for d in str(card_number)][::-1]
    checksum = sum(digits[0::2])
    for d in digits[1::2]:
        doubled = d * 2
        checksum += doubled if doubled < 10 else doubled - 9
    return checksum % 10 == 0

def get_card_info(card_number):
    """Get card type based on IIN (Issuer Identification Number)"""
    card_number = str(card_number)
    
    if re.match(r'^4[0-9]{12}(?:[0-9]{3})?$', card_number):
        return 'Visa'
    elif re.match(r'^5[1-5][0-9]{14}$', card_number):
        return 'MasterCard'
    elif re.match(r'^3[47][0-9]{13}$', card_number):
        return 'American Express'
    elif re.match(r'^6(?:011|5[0-9]{2})[0-9]{12}$', card_number):
        return 'Discover'
    else:
        return 'Unknown'

def validate_date(month, year):
    """Validate if the card expiration date is valid"""
    try:
        current_year = datetime.now().year % 100
        current_month = datetime.now().month
        
        month = int(month)
        year = int(year)
        
        if not (1 <= month <= 12):
            return False
            
        if year < current_year or (year == current_year and month < current_month):
            return False
            
        return True
    except ValueError:
        return False

def validate_cvv(cvv, card_type):
    """Validate CVV based on card type"""
    if card_type == 'American Express':
        return len(cvv) == 4
    return len(cvv) == 3

def create_loading_animation():
    """Create a loading animation"""
    with console.status("[bold green]Processing card details...", spinner="dots"):
        time.sleep(1.5)

def display_banner():
    """Display the program banner"""
    console.clear()
    art_text = text2art("CC Checker", font="block")
    console.print(f"[bold cyan]{art_text}[/bold cyan]")
    
    # Create author panel with GitHub link
    author_text = (
        "[bold yellow]Created by[/bold yellow] [bold cyan]Danish Khan[/bold cyan]\n"
        "[bold yellow]GitHub:[/bold yellow] [link=https://github.com/mavoio]https://github.com/mavoio[/link]"
    )
    author_panel = Panel(
        Align.center(author_text),
        border_style="bright_blue",
        title="[bold white]Author[/bold white]",
        title_align="center"
    )
    
    console.print(Align.center(author_panel))
    console.print(Align.center("[bold blue]The Ultimate Credit Card Validator[/bold blue]\n"))

def create_bin_info_table(bin_info):
    """Create a table with BIN information"""
    if not bin_info:
        return None
        
    bin_table = Table(box=box.ROUNDED, title="[bold magenta]BIN Information[/bold magenta]", 
                     title_style="bold magenta", border_style="bright_blue")
    bin_table.add_column("Detail", style="cyan")
    bin_table.add_column("Information", style="green")
    
    # Add available BIN information
    if bin_info.get("bank"):
        bin_table.add_row("Bank", bin_info["bank"].get("name", "Unknown"))
    if bin_info.get("country"):
        bin_table.add_row("Country", bin_info["country"].get("name", "Unknown"))
    if bin_info.get("scheme"):
        bin_table.add_row("Scheme", bin_info.get("scheme", "Unknown").upper())
    if bin_info.get("type"):
        bin_table.add_row("Card Type", bin_info.get("type", "Unknown").upper())
    if bin_info.get("brand"):
        bin_table.add_row("Brand", bin_info.get("brand", "Unknown"))
    if bin_info.get("prepaid") is not None:
        bin_table.add_row("Prepaid", "Yes" if bin_info["prepaid"] else "No")
        
    return bin_table

def main():
    display_banner()
    
    while True:
        console.print("\n[bold green]Enter card details in format[/bold green]:")
        console.print(Panel(
            "[cyan]number|mm/yy|cvv[/cyan] or [cyan]number|mm|yy|cvv[/cyan]",
            title="Input Format",
            border_style="green"
        ))
        console.print("[bold red]Enter 'exit' to quit[/bold red]\n")
        
        user_input = input("> ").strip()
        
        if user_input.lower() == 'exit':
            console.print("\n[bold yellow]Thank you for using CC Checker! Goodbye![/bold yellow]")
            time.sleep(1)
            console.clear()
            break
            
        # Parse input
        parts = user_input.split('|')
        if len(parts) != 3 and len(parts) != 4:
            console.print(Panel("[bold red]Invalid format! Please try again.[/bold red]", 
                              border_style="red"))
            continue
            
        # Extract card details
        card_number = ''.join(filter(str.isdigit, parts[0]))
        
        if len(parts) == 3:
            month, year = parts[1].split('/')
            cvv = parts[2]
        else:
            month, year = parts[1], parts[2]
            cvv = parts[3]
        
        create_loading_animation()
            
        # Validate card number using Luhn's algorithm
        is_valid = luhn_algorithm(card_number)
        card_type = get_card_info(card_number)
        
        # Get BIN information
        bin_info = get_bin_info(card_number)
        
        # Create main results table
        table = Table(box=box.ROUNDED, title="[bold blue]Card Validation Results[/bold blue]",
                     title_style="bold blue", border_style="bright_blue")
        table.add_column("Check", style="cyan")
        table.add_column("Result", style="green")
        
        # Add validation results with emojis
        table.add_row("Card Number", f"{card_number} [{'green' if is_valid else 'red'}]{'✓' if is_valid else '✗'}[/]")
        table.add_row("Card Type", f"{card_type} 💳")
        table.add_row("Luhn Check", f"{'✅ Valid' if is_valid else '❌ Invalid'}")
        
        # Validate expiration date
        date_valid = validate_date(month, year)
        table.add_row("Expiration", f"{month}/{year} {'✅' if date_valid else '❌'}")
        
        # Validate CVV
        cvv_valid = validate_cvv(cvv, card_type)
        table.add_row("CVV", f"{cvv} {'✅' if cvv_valid else '❌'}")
        
        # Display final result
        all_valid = is_valid and date_valid and cvv_valid
        result_color = "green" if all_valid else "red"
        result_text = "VALID" if all_valid else "INVALID"
        
        # Create layout
        layout = Layout()
        layout.split_column(
            Layout(name="upper"),
            Layout(name="lower")
        )
        
        # Add tables to layout
        layout["upper"].update(table)
        if bin_info:
            bin_table = create_bin_info_table(bin_info)
            if bin_table:
                layout["lower"].update(bin_table)
        
        console.print("\n")
        console.print(layout)
        
        # Display final result with animation
        with console.status("[bold yellow]Finalizing results...", spinner="dots"):
            time.sleep(0.5)
        
        result_panel = Panel(
            f"[bold {result_color}]Final Result: {result_text}[/bold {result_color}]",
            border_style=result_color,
            title="[bold white]Validation Status[/bold white]"
        )
        console.print("\n")
        console.print(Align.center(result_panel))

if __name__ == "__main__":
    main() 
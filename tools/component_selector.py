import tkinter as tk
from tkinter import ttk
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.component_library import component_database, ComponentStatus

class ComponentSelector:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Acoustic Manufacturing System - Component Selection Tool")
        self.window.geometry("900x700")
        
        # Create selection interface
        self.create_widgets()
        self.load_components()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Component category dropdown
        ttk.Label(main_frame, text="Component Category:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.category = ttk.Combobox(main_frame, values=[
            "All", "Acoustic", "Thermal", "Control", "Sensing"
        ], width=30)
        self.category.grid(row=0, column=1, sticky=tk.W, padx=10)
        self.category.set("All")
        self.category.bind("<<ComboboxSelected>>", self.filter_components)
        
        # Component selection
        ttk.Label(main_frame, text="Select Component:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.component_list = ttk.Combobox(main_frame, width=50)
        self.component_list.grid(row=1, column=1, sticky=tk.W, padx=10)
        self.component_list.bind("<<ComboboxSelected>>", self.display_component_details)
        
        # Requirements display
        ttk.Label(main_frame, text="Requirements:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.requirements_text = tk.Text(main_frame, height=5, width=60, wrap=tk.WORD)
        self.requirements_text.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
        
        # COTS Options frame
        options_frame = ttk.LabelFrame(main_frame, text="COTS Options", padding="10")
        options_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Options listbox
        self.options_listbox = tk.Listbox(options_frame, height=6, width=80)
        self.options_listbox.grid(row=0, column=0, columnspan=2)
        self.options_listbox.bind('<<ListboxSelect>>', self.display_option_details)
        
        # Option details
        ttk.Label(options_frame, text="Option Details:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.option_details = tk.Text(options_frame, height=8, width=80, wrap=tk.WORD)
        self.option_details.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Generate BOM", command=self.generate_bom).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Perform Trade Study", command=self.perform_trade_study).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Export Selection", command=self.export_selection).grid(row=0, column=2, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self.window, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.status_var.set("Ready")
        
    def load_components(self):
        """Load components from the database"""
        self.components = {}
        for comp_id, spec in component_database.items():
            self.components[f"{spec.name} ({comp_id})"] = spec
        self.filter_components()
        
    def filter_components(self, event=None):
        """Filter components by category"""
        category = self.category.get()
        filtered = []
        
        for name, spec in self.components.items():
            if category == "All" or spec.category == category:
                filtered.append(name)
        
        self.component_list['values'] = filtered
        if filtered:
            self.component_list.set(filtered[0])
            self.display_component_details()
    
    def display_component_details(self, event=None):
        """Display details for selected component"""
        selected = self.component_list.get()
        if not selected:
            return
            
        spec = self.components[selected]
        
        # Display requirements
        self.requirements_text.delete(1.0, tk.END)
        for key, value in spec.requirements.items():
            self.requirements_text.insert(tk.END, f"• {key}: {value}\n")
        
        # Display COTS options
        self.options_listbox.delete(0, tk.END)
        for i, option in enumerate(spec.cots_options):
            self.options_listbox.insert(tk.END, 
                f"{option.manufacturer} - {option.part_number} - ${option.unit_cost:,.2f} - Score: {option.score}")
        
        if spec.cots_options:
            self.options_listbox.selection_set(0)
            self.display_option_details()
    
    def display_option_details(self, event=None):
        """Display details for selected COTS option"""
        selection = self.options_listbox.curselection()
        if not selection:
            return
            
        selected_comp = self.component_list.get()
        spec = self.components[selected_comp]
        option = spec.cots_options[selection[0]]
        
        self.option_details.delete(1.0, tk.END)
        self.option_details.insert(tk.END, f"Manufacturer: {option.manufacturer}\n")
        self.option_details.insert(tk.END, f"Part Number: {option.part_number}\n")
        self.option_details.insert(tk.END, f"Description: {option.description}\n")
        self.option_details.insert(tk.END, f"Unit Cost: ${option.unit_cost:,.2f}\n")
        self.option_details.insert(tk.END, f"Lead Time: {option.lead_time_weeks} weeks\n")
        self.option_details.insert(tk.END, f"Min Order Qty: {option.min_order_qty}\n")
        self.option_details.insert(tk.END, f"\nTechnical Specs:\n")
        for key, value in option.technical_specs.items():
            self.option_details.insert(tk.END, f"  • {key}: {value}\n")
        self.option_details.insert(tk.END, f"\nPros: {', '.join(option.pros)}\n")
        self.option_details.insert(tk.END, f"Cons: {', '.join(option.cons)}\n")
    
    def generate_bom(self):
        """Generate BOM window"""
        bom_window = tk.Toplevel(self.window)
        bom_window.title("Bill of Materials Generator")
        bom_window.geometry("600x400")
        
        ttk.Label(bom_window, text="Select Level:", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=10, pady=10)
        level_var = tk.IntVar(value=1)
        for i in range(1, 5):
            ttk.Radiobutton(bom_window, text=f"Level {i}", variable=level_var, value=i).grid(row=0, column=i, padx=5)
        
        bom_text = tk.Text(bom_window, width=80, height=20)
        bom_text.grid(row=1, column=0, columnspan=5, padx=10, pady=10)
        
        def update_bom():
            from models.component_library import generate_bom
            level = level_var.get()
            bom_df = generate_bom(level)
            bom_text.delete(1.0, tk.END)
            bom_text.insert(tk.END, f"LEVEL {level} BILL OF MATERIALS\n")
            bom_text.insert(tk.END, "="*60 + "\n")
            bom_text.insert(tk.END, bom_df.to_string(index=False))
            
            # Calculate total cost
            total = sum([float(cost.replace('$', '').replace(',', '')) 
                        for cost in bom_df['Extended Cost']])
            bom_text.insert(tk.END, f"\n\nTOTAL COST: ${total:,.2f}")
        
        ttk.Button(bom_window, text="Generate", command=update_bom).grid(row=2, column=2, pady=10)
        update_bom()
    
    def perform_trade_study(self):
        """Perform trade study for selected component"""
        selected = self.component_list.get()
        if not selected:
            self.status_var.set("Please select a component first")
            return
            
        spec = self.components[selected]
        comp_id = selected.split('(')[1].rstrip(')')
        
        from models.component_library import perform_trade_study
        trade_df = perform_trade_study(comp_id)
        
        # Create trade study window
        trade_window = tk.Toplevel(self.window)
        trade_window.title(f"Trade Study: {spec.name}")
        trade_window.geometry("800x400")
        
        trade_text = tk.Text(trade_window, width=100, height=25)
        trade_text.pack(padx=10, pady=10)
        
        trade_text.insert(tk.END, f"TRADE STUDY: {spec.name}\n")
        trade_text.insert(tk.END, "="*80 + "\n")
        trade_text.insert(tk.END, trade_df.to_string(index=False))
        
        self.status_var.set(f"Trade study generated for {spec.name}")
    
    def export_selection(self):
        """Export current selection to JSON"""
        import json
        from datetime import datetime
        
        selected = self.component_list.get()
        if not selected:
            self.status_var.set("Please select a component first")
            return
            
        spec = self.components[selected]
        
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "component": {
                "id": spec.id,
                "name": spec.name,
                "category": spec.category,
                "requirements": spec.requirements,
                "selected_option": None
            }
        }
        
        selection = self.options_listbox.curselection()
        if selection:
            option = spec.cots_options[selection[0]]
            export_data["component"]["selected_option"] = {
                "manufacturer": option.manufacturer,
                "part_number": option.part_number,
                "unit_cost": option.unit_cost,
                "lead_time_weeks": option.lead_time_weeks
            }
        
        filename = f"selection_{spec.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        self.status_var.set(f"Selection exported to {filename}")
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ComponentSelector()
    app.run()
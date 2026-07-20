import tkinter as tk
from tkinter import ttk, messagebox
import math

class ElectricityBillTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Electricity Bill Generator & Power Tracker")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configure style
        self.root.configure(bg='#f0f0f0')
        
        # Data storage for appliances
        self.appliances = []
        self.rate_per_kwh = 7.0  # Default rate: ₹7 per kWh
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the main user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="⚡ Electricity Bill Generator", 
                              font=('Arial', 18, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Input section
        self.create_input_section(main_frame)
        
        # Appliances list section
        self.create_appliances_section(main_frame)
        
        # Summary section
        self.create_summary_section(main_frame)
        
        # Control buttons
        self.create_control_buttons(main_frame)
        
    def create_input_section(self, parent):
        """Create the appliance input section"""
        input_frame = tk.LabelFrame(parent, text="Add New Appliance", 
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0', 
                                   fg='#34495e', padx=15, pady=15)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create input fields in a grid
        tk.Label(input_frame, text="Appliance Name:", bg='#f0f0f0').grid(row=0, column=0, sticky='w', pady=5)
        self.name_entry = tk.Entry(input_frame, width=20, font=('Arial', 10))
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(input_frame, text="Power Rating (Watts):", bg='#f0f0f0').grid(row=0, column=2, sticky='w', pady=5)
        self.power_entry = tk.Entry(input_frame, width=15, font=('Arial', 10))
        self.power_entry.grid(row=0, column=3, padx=10, pady=5)
        
        tk.Label(input_frame, text="Daily Usage (Hours):", bg='#f0f0f0').grid(row=1, column=0, sticky='w', pady=5)
        self.hours_entry = tk.Entry(input_frame, width=15, font=('Arial', 10))
        self.hours_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(input_frame, text="Number of Days:", bg='#f0f0f0').grid(row=1, column=2, sticky='w', pady=5)
        self.days_entry = tk.Entry(input_frame, width=15, font=('Arial', 10))
        self.days_entry.grid(row=1, column=3, padx=10, pady=5)
        
        # Add button
        add_btn = tk.Button(input_frame, text="Add Appliance", command=self.add_appliance,
                           bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                           padx=20, pady=5, cursor='hand2')
        add_btn.grid(row=2, column=1, columnspan=2, pady=15)
        
        # Rate setting
        rate_frame = tk.Frame(input_frame, bg='#f0f0f0')
        rate_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        tk.Label(rate_frame, text="Rate per kWh (₹):", bg='#f0f0f0').pack(side=tk.LEFT)
        self.rate_entry = tk.Entry(rate_frame, width=10, font=('Arial', 10))
        self.rate_entry.pack(side=tk.LEFT, padx=10)
        self.rate_entry.insert(0, str(self.rate_per_kwh))
        
        rate_btn = tk.Button(rate_frame, text="Update Rate", command=self.update_rate,
                            bg='#e67e22', fg='white', font=('Arial', 9),
                            padx=10, pady=2, cursor='hand2')
        rate_btn.pack(side=tk.LEFT, padx=10)
        
    def create_appliances_section(self, parent):
        """Create the appliances list section"""
        list_frame = tk.LabelFrame(parent, text="Added Appliances", 
                                  font=('Arial', 12, 'bold'), bg='#f0f0f0', 
                                  fg='#34495e', padx=15, pady=15)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Create treeview for appliances list
        columns = ('Name', 'Power (W)', 'Hours/Day', 'Days', 'Energy (kWh)', 'Cost (₹)')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        
        # Define column headings and widths
        column_widths = [120, 80, 80, 60, 100, 100]
        for i, col in enumerate(columns):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths[i], anchor='center')
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Delete button
        delete_btn = tk.Button(list_frame, text="Delete Selected", command=self.delete_appliance,
                              bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                              padx=15, pady=5, cursor='hand2')
        delete_btn.pack(pady=10)
        
    def create_summary_section(self, parent):
        """Create the summary section"""
        summary_frame = tk.LabelFrame(parent, text="Bill Summary", 
                                     font=('Arial', 12, 'bold'), bg='#f0f0f0', 
                                     fg='#34495e', padx=15, pady=15)
        summary_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Summary labels
        self.total_energy_label = tk.Label(summary_frame, text="Total Energy Consumption: 0.00 kWh", 
                                          font=('Arial', 11, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        self.total_energy_label.pack(pady=5)
        
        self.total_cost_label = tk.Label(summary_frame, text="Total Electricity Bill: ₹0.00", 
                                        font=('Arial', 14, 'bold'), bg='#f0f0f0', fg='#27ae60')
        self.total_cost_label.pack(pady=5)
        
        self.avg_daily_label = tk.Label(summary_frame, text="Average Daily Consumption: 0.00 kWh", 
                                       font=('Arial', 10), bg='#f0f0f0', fg='#7f8c8d')
        self.avg_daily_label.pack(pady=2)
        
    def create_control_buttons(self, parent):
        """Create control buttons"""
        button_frame = tk.Frame(parent, bg='#f0f0f0')
        button_frame.pack(fill=tk.X)
        
        # Calculate button
        calc_btn = tk.Button(button_frame, text="Calculate Bill", command=self.calculate_bill,
                            bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                            padx=30, pady=10, cursor='hand2')
        calc_btn.pack(side=tk.LEFT, padx=10)
        
        # Clear all button
        clear_btn = tk.Button(button_frame, text="Clear All", command=self.clear_all,
                             bg='#95a5a6', fg='white', font=('Arial', 12, 'bold'),
                             padx=30, pady=10, cursor='hand2')
        clear_btn.pack(side=tk.LEFT, padx=10)
        
        # Export button (saves to text file)
        export_btn = tk.Button(button_frame, text="Export Report", command=self.export_report,
                              bg='#8e44ad', fg='white', font=('Arial', 12, 'bold'),
                              padx=30, pady=10, cursor='hand2')
        export_btn.pack(side=tk.RIGHT, padx=10)
        
    def add_appliance(self):
        """Add a new appliance to the list"""
        try:
            # Get input values
            name = self.name_entry.get().strip()
            power = float(self.power_entry.get())
            hours = float(self.hours_entry.get())
            days = int(self.days_entry.get())
            
            # Validate inputs
            if not name:
                messagebox.showerror("Error", "Please enter appliance name!")
                return
            if power <= 0 or hours <= 0 or days <= 0:
                messagebox.showerror("Error", "Power, hours, and days must be positive values!")
                return
            if hours > 24:
                messagebox.showerror("Error", "Daily usage cannot exceed 24 hours!")
                return
                
            # Calculate energy consumption in kWh
            energy_kwh = (power * hours * days) / 1000
            cost = energy_kwh * self.rate_per_kwh
            
            # Create appliance dictionary
            appliance = {
                'name': name,
                'power': power,
                'hours': hours,
                'days': days,
                'energy_kwh': energy_kwh,
                'cost': cost
            }
            
            # Add to list
            self.appliances.append(appliance)
            
            # Add to treeview
            self.tree.insert('', tk.END, values=(
                name, f"{power:.0f}", f"{hours:.1f}", days, 
                f"{energy_kwh:.2f}", f"{cost:.2f}"
            ))
            
            # Clear input fields
            self.clear_inputs()
            
            # Update summary
            self.update_summary()
            
            messagebox.showinfo("Success", f"Added {name} successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def delete_appliance(self):
        """Delete selected appliance"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an appliance to delete!")
            return
        
        # Get the index of selected item
        item = selected[0]
        index = self.tree.index(item)
        
        # Remove from data and treeview
        self.appliances.pop(index)
        self.tree.delete(item)
        
        # Update summary
        self.update_summary()
        
        messagebox.showinfo("Success", "Appliance deleted successfully!")
    
    def update_rate(self):
        """Update the rate per kWh"""
        try:
            new_rate = float(self.rate_entry.get())
            if new_rate <= 0:
                messagebox.showerror("Error", "Rate must be a positive value!")
                return
            
            self.rate_per_kwh = new_rate
            
            # Recalculate costs for existing appliances
            for i, appliance in enumerate(self.appliances):
                appliance['cost'] = appliance['energy_kwh'] * self.rate_per_kwh
                
                # Update treeview
                item = self.tree.get_children()[i]
                values = list(self.tree.item(item)['values'])
                values[5] = f"{appliance['cost']:.2f}"
                self.tree.item(item, values=values)
            
            self.update_summary()
            messagebox.showinfo("Success", f"Rate updated to ₹{new_rate:.2f}/kWh")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid rate!")
    
    def calculate_bill(self):
        """Calculate and display the total bill"""
        if not self.appliances:
            messagebox.showwarning("Warning", "Please add some appliances first!")
            return
        
        total_energy = sum(app['energy_kwh'] for app in self.appliances)
        total_cost = sum(app['cost'] for app in self.appliances)
        
        # Show detailed calculation
        details = "Electricity Bill Calculation\n" + "="*40 + "\n\n"
        
        for app in self.appliances:
            details += f"{app['name']}:\n"
            details += f"  Power: {app['power']:.0f}W\n"
            details += f"  Usage: {app['hours']:.1f} hours/day × {app['days']} days\n"
            details += f"  Energy: {app['energy_kwh']:.2f} kWh\n"
            details += f"  Cost: ₹{app['cost']:.2f}\n\n"
        
        details += f"Total Energy Consumption: {total_energy:.2f} kWh\n"
        details += f"Rate: ₹{self.rate_per_kwh:.2f}/kWh\n"
        details += f"Total Bill Amount: ₹{total_cost:.2f}"
        
        # Show in a new window
        self.show_calculation_window(details)
    
    def show_calculation_window(self, details):
        """Show calculation details in a new window"""
        calc_window = tk.Toplevel(self.root)
        calc_window.title("Bill Calculation Details")
        calc_window.geometry("400x500")
        calc_window.configure(bg='#f0f0f0')
        
        # Text widget with scrollbar
        text_frame = tk.Frame(calc_window, bg='#f0f0f0')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Courier', 10), 
                             bg='white', fg='#2c3e50')
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget.insert(tk.END, details)
        text_widget.config(state=tk.DISABLED)
        
        # Close button
        close_btn = tk.Button(calc_window, text="Close", command=calc_window.destroy,
                             bg='#34495e', fg='white', font=('Arial', 11, 'bold'),
                             padx=20, pady=5)
        close_btn.pack(pady=10)
    
    def update_summary(self):
        """Update the summary section"""
        if not self.appliances:
            self.total_energy_label.config(text="Total Energy Consumption: 0.00 kWh")
            self.total_cost_label.config(text="Total Electricity Bill: ₹0.00")
            self.avg_daily_label.config(text="Average Daily Consumption: 0.00 kWh")
            return
        
        total_energy = sum(app['energy_kwh'] for app in self.appliances)
        total_cost = sum(app['cost'] for app in self.appliances)
        total_days = sum(app['days'] for app in self.appliances)
        avg_daily = total_energy / len(self.appliances) if self.appliances else 0
        
        self.total_energy_label.config(text=f"Total Energy Consumption: {total_energy:.2f} kWh")
        self.total_cost_label.config(text=f"Total Electricity Bill: ₹{total_cost:.2f}")
        self.avg_daily_label.config(text=f"Average Daily Consumption: {avg_daily:.2f} kWh")
    
    def clear_inputs(self):
        """Clear all input fields"""
        self.name_entry.delete(0, tk.END)
        self.power_entry.delete(0, tk.END)
        self.hours_entry.delete(0, tk.END)
        self.days_entry.delete(0, tk.END)
    
    def clear_all(self):
        """Clear all appliances"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all appliances?"):
            self.appliances.clear()
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.update_summary()
            messagebox.showinfo("Success", "All appliances cleared!")
    
    def export_report(self):
        """Export the bill report to a text file"""
        if not self.appliances:
            messagebox.showwarning("Warning", "No appliances to export!")
            return
        
        try:
            with open("electricity_bill_report.txt", "w") as f:
                f.write("ELECTRICITY BILL REPORT\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Rate per kWh: ₹{self.rate_per_kwh:.2f}\n\n")
                
                f.write("APPLIANCE DETAILS:\n")
                f.write("-" * 50 + "\n")
                
                total_energy = 0
                total_cost = 0
                
                for i, app in enumerate(self.appliances, 1):
                    f.write(f"{i}. {app['name']}\n")
                    f.write(f"   Power Rating: {app['power']:.0f} Watts\n")
                    f.write(f"   Daily Usage: {app['hours']:.1f} hours\n")
                    f.write(f"   Number of Days: {app['days']}\n")
                    f.write(f"   Energy Consumption: {app['energy_kwh']:.2f} kWh\n")
                    f.write(f"   Cost: ₹{app['cost']:.2f}\n\n")
                    
                    total_energy += app['energy_kwh']
                    total_cost += app['cost']
                
                f.write("SUMMARY:\n")
                f.write("-" * 50 + "\n")
                f.write(f"Total Energy Consumption: {total_energy:.2f} kWh\n")
                f.write(f"Total Bill Amount: ₹{total_cost:.2f}\n")
                f.write(f"Average per Appliance: ₹{total_cost/len(self.appliances):.2f}\n")
            
            messagebox.showinfo("Success", "Report exported to 'electricity_bill_report.txt'")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = ElectricityBillTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
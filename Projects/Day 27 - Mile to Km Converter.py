import tkinter as tk


def miles_to_km():
    '''Convert miles to kilometers'''
    miles = input.get()
    km = float(miles) * 1.609
    # Update the label with the converted value
    label_number.config(text=f"{round(km, 1)}")


window = tk.Tk()
window.title("Mile to Km Converter")
window.config(padx=20, pady=20)

# Entry component for input
input = tk.Entry(width=10)
input.grid(row=0, column=1)

# Labels
label_miles = tk.Label(text="Miles")
label_miles.grid(row=0, column=2)

label_is_equal_to = tk.Label(text="is equal to")
label_is_equal_to.grid(row=1, column=0)

label_number = tk.Label(text="0")
label_number.grid(row=1, column=1)

label_km = tk.Label(text="Km")
label_km.grid(row=1, column=2)

# Button to trigger the conversion
button = tk.Button(text="Calculate", command=miles_to_km)
button.grid(row=2, column=1)

window.mainloop()

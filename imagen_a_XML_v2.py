import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinter.ttk import Progressbar
from PIL import Image
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        self.root.geometry("600x400")  # Ajusta el tamaño inicial de la ventana

        # Widgets
        self.label_status = ttk.Label(root, text="Seleccione una carpeta para comenzar:")
        self.label_status.grid(row=0, column=0, columnspan=2, pady=10)

        self.button_select_folder = ttk.Button(root, text="Seleccionar Carpeta", command=self.select_folder)
        self.button_select_folder.grid(row=1, column=0, pady=10)

        self.progress = Progressbar(root, orient=tk.HORIZONTAL, length=100, mode='indeterminate')
        self.progress.grid(row=1, column=1, pady=10)

        self.log_console = scrolledtext.ScrolledText(root, height=10, state='disabled')
        self.log_console.grid(row=2, column=0, columnspan=2, pady=10)

        self.image_count = 0  # Inicializa el contador de imágenes

    def log_message(self, message):
        self.log_console.config(state='normal')
        self.log_console.insert(tk.END, message + "\n")
        self.log_console.config(state='disabled')
        self.log_console.see(tk.END)

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.label_status.config(text="Procesando...")
            self.image_count = 0  # Reinicia el contador cada vez que se selecciona una nueva carpeta
            self.progress.start(10)
            self.process_images()

    def process_images(self):
        root_xml = ET.Element('Imagenes')
        try:
            for subdir, dirs, files in os.walk(self.folder_path):
                for file in files:
                    if file.endswith(('.png', '.jpg', '.jpeg')):
                        self.classify_and_add_to_xml(root_xml, os.path.join(subdir, file))
            self.write_xml_file(root_xml)
            messagebox.showinfo("Éxito", "Archivo XML generado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.progress.stop()
            self.label_status.config(text="Seleccione una carpeta para comenzar:")

    def classify_and_add_to_xml(self, root_xml, file_path):
        image = Image.open(file_path)
        width, height = image.size
        ratio = width / height

        # Ajuste de la heurística para clasificar más ampliamente
        image_type = "Imágen/Fotografía/Yacimiento/Museo"
        if ratio < 0.75 or ratio > 1.33:  #Se ajusta así para diferenciar los planos de las imágenes normales
            image_type = "Plano"
        
        image_element = ET.SubElement(root_xml, 'Imageb')
        ET.SubElement(image_element, 'ID').text = str(self.image_count + 1)
        ET.SubElement(image_element, 'ID_ENTRADA').text = str(self.image_count + 100)
        ET.SubElement(image_element, 'ARCHIVO').text = os.path.basename(file_path)
        ET.SubElement(image_element, 'RUTA').text = file_path
        ET.SubElement(image_element, 'TIPO').text = image_type

        self.image_count += 1  # Incrementa el contador después de procesar cada imagen

    def write_xml_file(self, root_xml):
        xml_string = ET.tostring(root_xml, 'utf-8')
        parsed_string = parseString(xml_string)
        pretty_xml_as_string = parsed_string.toprettyxml(indent="  ", encoding='UTF-8')

        output_path = os.path.join(self.folder_path, 'Archivo.xml')
        with open(output_path, 'wb') as xml_file:
            xml_file.write(pretty_xml_as_string)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()






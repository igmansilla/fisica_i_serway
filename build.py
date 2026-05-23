#!/usr/bin/env python3
import os
import subprocess
import shutil
import argparse

base_dir = "/home/ignacio/personas/fisica_i_serway"
output_dir = os.path.join(base_dir, "pdfs")

targets = {
    "capitulo_01": {
        "tex_path": os.path.join(base_dir, "capitulo_01.tex"),
        "working_dir": base_dir,
        "dest_name": "Fisica_I_Capitulo_01.pdf",
        "description": "Capítulo 1 completo con espacios"
    },
    "capitulo_02": {
        "tex_path": os.path.join(base_dir, "capitulo_02.tex"),
        "working_dir": base_dir,
        "dest_name": "Fisica_I_Capitulo_02.pdf",
        "description": "Capítulo 2 completo con espacios"
    },
    "capitulo_03": {
        "tex_path": os.path.join(base_dir, "capitulo_03.tex"),
        "working_dir": base_dir,
        "dest_name": "Fisica_I_Capitulo_03.pdf",
        "description": "Capítulo 3 completo con espacios"
    },
    "capitulo_04": {
        "tex_path": os.path.join(base_dir, "capitulo_04.tex"),
        "working_dir": base_dir,
        "dest_name": "Fisica_I_Capitulo_04.pdf",
        "description": "Capítulo 4 completo con espacios"
    },
    "capitulo_05": {
        "tex_path": os.path.join(base_dir, "capitulo_05.tex"),
        "working_dir": base_dir,
        "dest_name": "Fisica_I_Capitulo_05.pdf",
        "description": "Capítulo 5 completo con espacios"
    },
    "capitulo_06": {
        "tex_path": os.path.join(base_dir, "capitulo_06.tex"),
        "working_dir": base_dir,
        "dest_name": "Fisica_I_Capitulo_06.pdf",
        "description": "Capítulo 6 completo con espacios"
    },
    "ejercicios_preparacion": {
        "tex_path": os.path.join(base_dir, "ejercicios_preparacion.tex"),
        "working_dir": base_dir,
        "dest_name": "Fisica_I_Ejercicios_Preparacion.pdf",
        "description": "Serie de ejercicios seleccionados para preparar examen"
    },
    "examenes_practica": {
        "tex_path": os.path.join(base_dir, "examenes_practica.tex"),
        "working_dir": base_dir,
        "dest_name": "Fisica_I_Examenes_Practica.pdf",
        "description": "Exámenes de práctica (Examen 1 y Examen 2)"
    }
}

def compile_latex(tex_path, working_dir, dest_name):
    print(f"\n🚀 Compilando: {os.path.basename(tex_path)}...")
    
    # Run pdflatex (2 passes for TOC and references to build successfully)
    for pass_num in range(1, 3):
        print(f"   Paso {pass_num}/2...")
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", os.path.basename(tex_path)],
            cwd=working_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )
        
        if result.returncode != 0:
            print(f"❌ Error al compilar {os.path.basename(tex_path)}:")
            # If log file exists, print the last 20 lines to help diagnose
            log_path = tex_path.replace(".tex", ".log")
            if os.path.exists(log_path):
                with open(log_path, "r", encoding="utf-8", errors="ignore") as log:
                    lines = log.readlines()
                    print("".join(lines[-20:]))
            return False
            
    # Locate the generated PDF
    pdf_name = os.path.basename(tex_path).replace(".tex", ".pdf")
    generated_pdf = os.path.join(working_dir, pdf_name)
    
    if os.path.exists(generated_pdf):
        os.makedirs(output_dir, exist_ok=True)
        destination = os.path.join(output_dir, dest_name)
        shutil.copy2(generated_pdf, destination)
        print(f"✅ ¡Éxito! PDF guardado en: pdfs/{dest_name}")
        return True
    else:
        print("❌ Error: No se encontró el archivo PDF resultante.")
        return False

def clean_temp_files():
    print("\n🧹 Limpiando archivos auxiliares de LaTeX...")
    extensions = [".aux", ".log", ".out", ".toc", ".pdf"]
    for target in targets.values():
        wdir = target["working_dir"]
        tex_file = os.path.basename(target["tex_path"])
        base_name = tex_file.replace(".tex", "")
        
        for ext in extensions:
            temp_file = os.path.join(wdir, base_name + ext)
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception:
                    pass

def main():
    parser = argparse.ArgumentParser(description="Automatizador de compilación para Física I (Serway)")
    parser.add_argument("--target", choices=list(targets.keys()) + ["all"], default="all",
                        help="Compilar un objetivo específico o 'all' (por defecto)")
    parser.add_argument("--clean", action="store_true", help="Limpiar archivos temporales de LaTeX")
    
    args = parser.parse_args()
    
    # Check if pdflatex is installed
    if not shutil.which("pdflatex"):
        print("❌ Error: 'pdflatex' no está instalado en este sistema. Por favor instala TexLive o similar.")
        return

    if args.clean:
        clean_temp_files()
        print("✨ Limpieza completada.")
        return

    if args.target == "all":
        print("📚 Iniciando compilación de todos los objetivos...")
        success_count = 0
        for name, spec in targets.items():
            if compile_latex(spec["tex_path"], spec["working_dir"], spec["dest_name"]):
                success_count += 1
        
        # Cleanup temp files after compilation
        clean_temp_files()
        
        print(f"\n🎉 ¡Proceso finalizado! Compilados exitosamente: {success_count}/{len(targets)}")
        if success_count > 0:
            print(f"📂 Encuentra todos tus PDFs en la carpeta: {output_dir}")
    else:
        spec = targets[args.target]
        if compile_latex(spec["tex_path"], spec["working_dir"], spec["dest_name"]):
            clean_temp_files()

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
Sistema de Inspeção de Equipamentos - Interface Gráfica
Baseado no projeto React original, implementado em Python com Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import os
from datetime import datetime
from typing import Dict, Any, Optional

# Importar nossos módulos
from opcoes_formulario import get_todas_opcoes, get_estado_inicial, get_tags_por_tipo
from database import InspectionDatabase
from date_validator import DateValidator, is_vencido, add_days, format_date
from photo_handler import PhotoHandler, PhotoPreview
from report_generator import InspectionReportGenerator

class InspectionFormApp:
    """Aplicação principal do sistema de inspeção"""
    
    def __init__(self):
        """Inicializa a aplicação"""
        self.root = tk.Tk()
        self.setup_main_window()
        self.setup_variables()
        self.setup_ui()
        self.setup_photo_handler()
        self.setup_database()
        self.setup_report_generator()
        
    def setup_main_window(self):
        """Configura a janela principal"""
        self.root.title("🔍 Sistema de Inspeção de Equipamentos")
        self.root.geometry("1000x800")
        self.root.minsize(900, 700)
        
        # Centralizar janela
        self.root.eval('tk::PlaceWindow . center')
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar cores
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#2c3e50'
        }
        
    def setup_variables(self):
        """Configura as variáveis de controle"""
        self.opcoes = get_todas_opcoes()
        self.estado_atual = get_estado_inicial()
        
        # Variáveis para os campos
        self.plataforma_var = tk.StringVar()
        self.modulo_var = tk.StringVar()
        self.setor_var = tk.StringVar()
        self.tipo_equipamento_var = tk.StringVar()
        self.tag_var = tk.StringVar()
        self.defeito_var = tk.StringVar()
        self.causa_var = tk.StringVar()
        self.categoria_rti_var = tk.StringVar()
        self.recomendacao_var = tk.StringVar()
        self.ultima_var = tk.StringVar()
        self.data_var = tk.StringVar()
        self.tipo_dano_var = tk.StringVar()
        self.observacoes_var = tk.StringVar()
        
        # Configurar data atual
        self.data_var.set(datetime.now().strftime('%Y-%m-%d'))
        
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="🔍 SISTEMA DE INSPEÇÃO DE EQUIPAMENTOS", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame do formulário
        form_frame = ttk.LabelFrame(main_frame, text="📋 Dados da Inspeção", padding="15")
        form_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        form_frame.columnconfigure(1, weight=1)
        
        # Primeira linha - Plataforma, Módulo, Setor
        self.create_field_row(form_frame, 0, "Plataforma:", self.plataforma_var, 
                             self.opcoes['plataforma'], 'combobox')
        self.create_field_row(form_frame, 1, "Módulo:", self.modulo_var, 
                             self.opcoes['modulo'], 'combobox')
        self.create_field_row(form_frame, 2, "Setor:", self.setor_var, 
                             self.opcoes['setor'], 'combobox')
        
        # Segunda linha - Tipo de Equipamento e TAG
        self.create_field_row(form_frame, 3, "Tipo de Equipamento:", self.tipo_equipamento_var, 
                             self.opcoes['tipoEquipamento'], 'combobox')
        
        # TAG (será preenchida automaticamente)
        ttk.Label(form_frame, text="TAG:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.tag_entry = ttk.Entry(form_frame, textvariable=self.tag_var, state='readonly')
        self.tag_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Terceira linha - Datas
        self.create_field_row(form_frame, 5, "Data da Última Inspeção:", self.ultima_var, 
                             None, 'date')
        self.create_field_row(form_frame, 6, "Data da Inspeção Atual:", self.data_var, 
                             None, 'date')
        
        # Quarta linha - Tipo de Dano e Defeito
        self.create_field_row(form_frame, 7, "Tipo de Dano:", self.tipo_dano_var, 
                             self.opcoes['tipoDano'], 'combobox')
        self.create_field_row(form_frame, 8, "Defeito:", self.defeito_var, 
                             self.opcoes['defeito'], 'combobox')
        
        # Quinta linha - Causa e Categoria RTI
        self.create_field_row(form_frame, 9, "Causa:", self.causa_var, 
                             self.opcoes['causa'], 'combobox')
        self.create_field_row(form_frame, 10, "Categoria RTI:", self.categoria_rti_var, 
                             self.opcoes['categoriaRTI'], 'combobox')
        
        # Sexta linha - Recomendação
        self.create_field_row(form_frame, 11, "Recomendação:", self.recomendacao_var, 
                             self.opcoes['recomendacao'], 'combobox')
        
        # Sétima linha - Observações
        ttk.Label(form_frame, text="Observações:").grid(row=12, column=0, sticky=tk.W, pady=5)
        self.observacoes_text = ScrolledText(form_frame, height=4, width=50)
        self.observacoes_text.grid(row=12, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Oitava linha - Foto
        ttk.Label(form_frame, text="📸 Foto:").grid(row=13, column=0, sticky=tk.W, pady=5)
        photo_frame = ttk.Frame(form_frame)
        photo_frame.grid(row=13, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        self.select_photo_btn = ttk.Button(photo_frame, text="Selecionar Foto", 
                                          command=self.select_photo)
        self.select_photo_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_photo_btn = ttk.Button(photo_frame, text="Limpar Foto", 
                                         command=self.clear_photo)
        self.clear_photo_btn.pack(side=tk.LEFT)
        
        # Preview da foto
        self.photo_preview_frame = ttk.Frame(form_frame)
        self.photo_preview_frame.grid(row=14, column=0, columnspan=2, pady=10)
        
        # Status da inspeção
        self.status_frame = ttk.LabelFrame(form_frame, text="📊 Status da Inspeção", padding="10")
        self.status_frame.grid(row=15, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        self.status_frame.columnconfigure(0, weight=1)
        
        self.status_label = ttk.Label(self.status_frame, text="Preencha a data da última inspeção para ver o status")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Botões de ação
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        self.save_btn = ttk.Button(button_frame, text="💾 Salvar & Gerar PDF", 
                                   command=self.save_inspection, style='Accent.TButton')
        self.save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = ttk.Button(button_frame, text="🗑️ Limpar Formulário", 
                                   command=self.clear_form)
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.view_all_btn = ttk.Button(button_frame, text="👁️ Ver Todas as Inspeções", 
                                      command=self.view_all_inspections)
        self.view_all_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.generate_batch_btn = ttk.Button(button_frame, text="📊 Gerar Relatórios em Lote", 
                                            command=self.generate_batch_reports)
        self.generate_batch_btn.pack(side=tk.LEFT)
        
        # Configurar eventos
        self.setup_events()
        
    def create_field_row(self, parent, row, label_text, variable, options, field_type):
        """Cria uma linha de campo no formulário"""
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=5)
        
        if field_type == 'combobox':
            if options:
                widget = ttk.Combobox(parent, textvariable=variable, values=options, state='readonly')
            else:
                widget = ttk.Entry(parent, textvariable=variable)
        elif field_type == 'date':
            widget = ttk.Entry(parent, textvariable=variable)
        else:
            widget = ttk.Entry(parent, textvariable=variable)
            
        widget.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
    def setup_events(self):
        """Configura os eventos dos campos"""
        # Atualizar TAG quando tipo de equipamento mudar
        self.tipo_equipamento_var.trace('w', self.on_tipo_equipamento_change)
        
        # Atualizar status quando data da última inspeção mudar
        self.ultima_var.trace('w', self.on_ultima_inspection_change)
        
        # Atalhos de teclado
        self.root.bind('<Control-s>', lambda e: self.save_inspection())
        self.root.bind('<Control-l>', lambda e: self.clear_form())
        self.root.bind('<Control-o>', lambda e: self.select_photo())
        
    def setup_photo_handler(self):
        """Configura o manipulador de fotos"""
        self.photo_handler = PhotoHandler()
        self.current_photo_path = None
        
    def setup_database(self):
        """Configura o banco de dados"""
        try:
            self.db = InspectionDatabase()
            print("✅ Banco de dados conectado")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco: {e}")
            
    def setup_report_generator(self):
        """Configura o gerador de relatórios"""
        try:
            self.report_generator = InspectionReportGenerator()
            print("✅ Gerador de relatórios configurado")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao configurar gerador de relatórios: {e}")
            
    def on_tipo_equipamento_change(self, *args):
        """Atualiza as TAGs disponíveis quando o tipo de equipamento muda"""
        tipo = self.tipo_equipamento_var.get()
        if tipo:
            tags = get_tags_por_tipo(tipo)
            # Limpar TAG atual
            self.tag_var.set('')
            
    def on_ultima_inspection_change(self, *args):
        """Atualiza o status quando a data da última inspeção muda"""
        ultima = self.ultima_var.get()
        if ultima:
            self.update_inspection_status(ultima)
            
    def update_inspection_status(self, ultima_data):
        """Atualiza o status da inspeção"""
        try:
            status_info = DateValidator.get_inspection_status(ultima_data, 12)
            
            # Criar texto do status
            status_text = f"""
📅 Última Inspeção: {status_info.get('last_inspection_formatted', 'N/A')}
⏰ Próxima Inspeção: {status_info.get('next_inspection_formatted', 'N/A')}
📊 Dias até Vencimento: {status_info.get('days_until_due', 'N/A')}
🔔 Status: {status_info.get('message', 'N/A')}
            """.strip()
            
            # Configurar cor baseada no status
            status = status_info.get('status', 'unknown')
            if status == 'overdue':
                color = self.colors['danger']
            elif status == 'warning':
                color = self.colors['warning']
            elif status == 'attention':
                color = self.colors['warning']
            else:
                color = self.colors['success']
                
            self.status_label.config(text=status_text, foreground=color)
            
        except Exception as e:
            self.status_label.config(text=f"Erro ao calcular status: {e}", 
                                   foreground=self.colors['danger'])
            
    def select_photo(self):
        """Seleciona uma foto"""
        try:
            photo_path = self.photo_handler.select_photo(self.root)
            if photo_path:
                self.current_photo_path = photo_path
                self.show_photo_preview(photo_path)
                messagebox.showinfo("Sucesso", "Foto selecionada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao selecionar foto: {e}")
            
    def show_photo_preview(self, photo_path):
        """Mostra preview da foto"""
        # Limpar preview anterior
        for widget in self.photo_preview_frame.winfo_children():
            widget.destroy()
            
        # Criar novo preview
        try:
            from PIL import Image, ImageTk
            
            # Abrir e redimensionar imagem
            with Image.open(photo_path) as img:
                img.thumbnail((200, 200), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # Label para exibir a foto
                photo_label = ttk.Label(self.photo_preview_frame, image=photo)
                photo_label.image = photo  # Manter referência
                photo_label.pack()
                
                # Nome do arquivo
                filename_label = ttk.Label(self.photo_preview_frame, 
                                         text=os.path.basename(photo_path))
                filename_label.pack()
                
        except Exception as e:
            error_label = ttk.Label(self.photo_preview_frame, 
                                   text=f"Erro ao carregar preview: {e}")
            error_label.pack()
            
    def clear_photo(self):
        """Limpa a foto selecionada"""
        self.current_photo_path = None
        for widget in self.photo_preview_frame.winfo_children():
            widget.destroy()
            
    def save_inspection(self):
        """Salva a inspeção e gera PDF"""
        try:
            # Validar campos obrigatórios
            if not self.validate_form():
                return
                
            # Coletar dados do formulário
            inspection_data = self.collect_form_data()
            
            # Salvar no banco de dados
            inspection_id = self.db.save_inspection(inspection_data)
            
            # Gerar PDF
            pdf_path = self.report_generator.generate_inspection_report(
                inspection_data, self.current_photo_path)
            
            # Mostrar sucesso
            messagebox.showinfo("Sucesso", 
                               f"Inspeção salva com ID: {inspection_id}\n"
                               f"PDF gerado: {os.path.basename(pdf_path)}")
            
            # Limpar formulário
            self.clear_form()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar inspeção: {e}")
            
    def validate_form(self):
        """Valida os campos obrigatórios"""
        required_fields = [
            ('plataforma', 'Plataforma'),
            ('modulo', 'Módulo'),
            ('setor', 'Setor'),
            ('tipoEquipamento', 'Tipo de Equipamento'),
            ('defeito', 'Defeito'),
            ('causa', 'Causa'),
            ('categoriaRTI', 'Categoria RTI'),
            ('recomendacao', 'Recomendação'),
            ('ultima', 'Data da Última Inspeção'),
            ('data', 'Data da Inspeção Atual'),
            ('tipoDano', 'Tipo de Dano')
        ]
        
        for field_var, field_name in required_fields:
            value = getattr(self, f"{field_var}_var").get().strip()
            if not value:
                messagebox.showerror("Validação", f"Campo '{field_name}' é obrigatório!")
                return False
                
        return True
        
    def collect_form_data(self):
        """Coleta os dados do formulário"""
        return {
            'plataforma': self.plataforma_var.get().strip(),
            'modulo': self.modulo_var.get().strip(),
            'setor': self.setor_var.get().strip(),
            'tipoEquipamento': self.tipo_equipamento_var.get().strip(),
            'tag': self.tag_var.get().strip(),
            'defeito': self.defeito_var.get().strip(),
            'causa': self.causa_var.get().strip(),
            'categoriaRTI': self.categoria_rti_var.get().strip(),
            'recomendacao': self.recomendacao_var.get().strip(),
            'ultima': self.ultima_var.get().strip(),
            'data': self.data_var.get().strip(),
            'tipoDano': self.tipo_dano_var.get().strip(),
            'observacoes': self.observacoes_text.get('1.0', tk.END).strip(),
            'foto_path': self.current_photo_path or ''
        }
        
    def clear_form(self):
        """Limpa o formulário"""
        # Limpar variáveis
        for var_name in ['plataforma_var', 'modulo_var', 'setor_var', 'tipo_equipamento_var',
                        'tag_var', 'defeito_var', 'causa_var', 'categoria_rti_var',
                        'recomendacao_var', 'ultima_var', 'data_var', 'tipo_dano_var']:
            getattr(self, var_name).set('')
            
        # Limpar observações
        self.observacoes_text.delete('1.0', tk.END)
        
        # Limpar foto
        self.clear_photo()
        
        # Resetar data atual
        self.data_var.set(datetime.now().strftime('%Y-%m-%d'))
        
        # Limpar status
        self.status_label.config(text="Preencha a data da última inspeção para ver o status",
                                foreground='black')
        
    def view_all_inspections(self):
        """Mostra todas as inspeções"""
        try:
            inspections = self.db.get_all_inspections()
            if not inspections:
                messagebox.showinfo("Informação", "Nenhuma inspeção encontrada.")
                return
                
            # Criar janela de visualização
            self.create_inspections_window(inspections)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar inspeções: {e}")
            
    def create_inspections_window(self, inspections):
        """Cria janela para visualizar inspeções"""
        window = tk.Toplevel(self.root)
        window.title("👁️ Todas as Inspeções")
        window.geometry("800x600")
        
        # Frame principal
        main_frame = ttk.Frame(window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text=f"📊 Total de Inspeções: {len(inspections)}",
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Treeview para as inspeções
        columns = ('ID', 'TAG', 'Tipo', 'Plataforma', 'Data', 'Status')
        tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=20)
        
        # Configurar colunas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
            
        # Adicionar dados
        for inspection in inspections:
            # Calcular status
            ultima = inspection.get('ultima_inspecao', '')
            if ultima:
                status_info = DateValidator.get_inspection_status(ultima, 12)
                status = status_info.get('message', 'N/A')
            else:
                status = 'N/A'
                
            tree.insert('', 'end', values=(
                inspection.get('id', 'N/A'),
                inspection.get('tag', 'N/A'),
                inspection.get('tipo_equipamento', 'N/A'),
                inspection.get('plataforma', 'N/A'),
                inspection.get('data_inspecao', 'N/A'),
                status
            ))
            
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="🔄 Atualizar", 
                  command=lambda: self.refresh_inspections(tree)).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="📊 Gerar Relatório Resumo", 
                  command=lambda: self.generate_summary_report(inspections)).pack(side=tk.LEFT)
        
    def refresh_inspections(self, tree):
        """Atualiza a lista de inspeções"""
        try:
            # Limpar tree
            for item in tree.get_children():
                tree.delete(item)
                
            # Buscar inspeções atualizadas
            inspections = self.db.get_all_inspections()
            
            # Adicionar dados atualizados
            for inspection in inspections:
                ultima = inspection.get('ultima_inspecao', '')
                if ultima:
                    status_info = DateValidator.get_inspection_status(ultima, 12)
                    status = status_info.get('message', 'N/A')
                else:
                    status = 'N/A'
                    
                tree.insert('', 'end', values=(
                    inspection.get('id', 'N/A'),
                    inspection.get('tag', 'N/A'),
                    inspection.get('tipo_equipamento', 'N/A'),
                    inspection.get('plataforma', 'N/A'),
                    inspection.get('data_inspecao', 'N/A'),
                    status
                ))
                
            messagebox.showinfo("Sucesso", "Lista atualizada!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar: {e}")
            
    def generate_batch_reports(self):
        """Gera relatórios em lote"""
        try:
            inspections = self.db.get_all_inspections()
            if not inspections:
                messagebox.showinfo("Informação", "Nenhuma inspeção encontrada para gerar relatórios.")
                return
                
            # Confirmar ação
            result = messagebox.askyesno("Confirmação", 
                                       f"Gerar relatórios para {len(inspections)} inspeções?\n"
                                       "Isso pode demorar alguns minutos.")
            if not result:
                return
                
            # Gerar relatórios
            pdf_files = self.report_generator.generate_batch_reports(inspections)
            
            messagebox.showinfo("Sucesso", 
                               f"Relatórios gerados com sucesso!\n"
                               f"Total: {len(pdf_files)} arquivos")
                               
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatórios em lote: {e}")
            
    def generate_summary_report(self, inspections):
        """Gera relatório resumo"""
        try:
            pdf_path = self.report_generator.generate_summary_report(inspections)
            
            messagebox.showinfo("Sucesso", 
                               f"Relatório resumo gerado!\n"
                               f"Arquivo: {os.path.basename(pdf_path)}")
                               
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório resumo: {e}")
            
    def run(self):
        """Executa a aplicação"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n🛑 Aplicação interrompida pelo usuário")
        finally:
            # Fechar conexões
            if hasattr(self, 'db'):
                self.db.close()

def main():
    """Função principal"""
    try:
        print("🚀 Iniciando Sistema de Inspeção de Equipamentos...")
        app = InspectionFormApp()
        app.run()
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        messagebox.showerror("Erro Fatal", f"Erro ao iniciar aplicação: {e}")

if __name__ == "__main__":
    main()

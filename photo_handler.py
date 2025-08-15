# -*- coding: utf-8 -*-
"""
Sistema de manipulação de fotos para inspeções
Substitui o sistema de upload do React
"""

import os
import shutil
from datetime import datetime
from typing import Optional, Tuple, List
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

class PhotoHandler:
    """Classe para manipulação de fotos"""
    
    def __init__(self, photos_dir: str = 'fotos_inspecoes'):
        """
        Inicializa o manipulador de fotos
        
        Args:
            photos_dir: Diretório para armazenar as fotos
        """
        self.photos_dir = photos_dir
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.max_dimensions = (1920, 1080)  # Máximo 1920x1080
        self.thumbnail_size = (300, 300)  # Tamanho do thumbnail
        
        # Criar diretório de fotos se não existir
        self._ensure_photos_directory()
    
    def _ensure_photos_directory(self):
        """Garante que o diretório de fotos existe"""
        try:
            if not os.path.exists(self.photos_dir):
                os.makedirs(self.photos_dir)
                print(f"✅ Diretório de fotos criado: {self.photos_dir}")
        except Exception as e:
            print(f"❌ Erro ao criar diretório de fotos: {e}")
            raise
    
    def select_photo(self, parent_window=None) -> Optional[str]:
        """
        Abre diálogo para seleção de foto
        
        Args:
            parent_window: Janela pai para o diálogo
            
        Returns:
            str: Caminho da foto selecionada ou None
        """
        try:
            file_path = filedialog.askopenfilename(
                parent=parent_window,
                title="Selecionar Foto",
                filetypes=[
                    ("Imagens", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff"),
                    ("JPEG", "*.jpg *.jpeg"),
                    ("PNG", "*.png"),
                    ("GIF", "*.gif"),
                    ("BMP", "*.bmp"),
                    ("TIFF", "*.tiff"),
                    ("Todos os arquivos", "*.*")
                ]
            )
            
            if file_path:
                return self.validate_and_process_photo(file_path)
            return None
            
        except Exception as e:
            print(f"❌ Erro ao selecionar foto: {e}")
            messagebox.showerror("Erro", f"Erro ao selecionar foto: {e}")
            return None
    
    def validate_and_process_photo(self, file_path: str) -> Optional[str]:
        """
        Valida e processa uma foto selecionada
        
        Args:
            file_path: Caminho da foto original
            
        Returns:
            str: Caminho da foto processada ou None
        """
        try:
            # Validar arquivo
            if not self._validate_photo_file(file_path):
                return None
            
            # Processar e salvar foto
            processed_path = self._process_and_save_photo(file_path)
            
            if processed_path:
                print(f"✅ Foto processada e salva: {processed_path}")
                return processed_path
            else:
                return None
                
        except Exception as e:
            print(f"❌ Erro ao processar foto: {e}")
            messagebox.showerror("Erro", f"Erro ao processar foto: {e}")
            return None
    
    def _validate_photo_file(self, file_path: str) -> bool:
        """
        Valida se o arquivo de foto é válido
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            bool: True se válido
        """
        try:
            # Verificar se arquivo existe
            if not os.path.exists(file_path):
                messagebox.showerror("Erro", "Arquivo não encontrado")
                return False
            
            # Verificar extensão
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext not in self.supported_formats:
                messagebox.showerror("Erro", f"Formato não suportado: {file_ext}")
                return False
            
            # Verificar tamanho do arquivo
            file_size = os.path.getsize(file_path)
            if file_size > self.max_file_size:
                messagebox.showerror("Erro", f"Arquivo muito grande: {file_size / (1024*1024):.1f}MB")
                return False
            
            # Verificar se é uma imagem válida
            try:
                with Image.open(file_path) as img:
                    img.verify()
            except Exception:
                messagebox.showerror("Erro", "Arquivo não é uma imagem válida")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na validação: {e}")
            return False
    
    def _process_and_save_photo(self, original_path: str) -> Optional[str]:
        """
        Processa e salva a foto
        
        Args:
            original_path: Caminho da foto original
            
        Returns:
            str: Caminho da foto processada
        """
        try:
            # Abrir imagem
            with Image.open(original_path) as img:
                # Converter para RGB se necessário
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Redimensionar se muito grande
                if img.width > self.max_dimensions[0] or img.height > self.max_dimensions[1]:
                    img.thumbnail(self.max_dimensions, Image.Resampling.LANCZOS)
                
                # Gerar nome único para o arquivo
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                original_name = os.path.splitext(os.path.basename(original_path))[0]
                new_filename = f"{original_name}_{timestamp}.jpg"
                new_path = os.path.join(self.photos_dir, new_filename)
                
                # Salvar como JPEG com qualidade otimizada
                img.save(new_path, 'JPEG', quality=85, optimize=True)
                
                return new_path
                
        except Exception as e:
            print(f"❌ Erro ao processar foto: {e}")
            return None
    
    def create_thumbnail(self, photo_path: str, size: Tuple[int, int] = None) -> Optional[str]:
        """
        Cria um thumbnail da foto
        
        Args:
            photo_path: Caminho da foto original
            size: Tamanho do thumbnail (largura, altura)
            
        Returns:
            str: Caminho do thumbnail criado
        """
        try:
            if not size:
                size = self.thumbnail_size
            
            with Image.open(photo_path) as img:
                # Manter proporção
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                # Gerar nome do thumbnail
                dir_path = os.path.dirname(photo_path)
                filename = os.path.basename(photo_path)
                name, ext = os.path.splitext(filename)
                thumbnail_name = f"{name}_thumb{ext}"
                thumbnail_path = os.path.join(dir_path, thumbnail_name)
                
                # Salvar thumbnail
                img.save(thumbnail_path, 'JPEG', quality=80)
                
                return thumbnail_path
                
        except Exception as e:
            print(f"❌ Erro ao criar thumbnail: {e}")
            return None
    
    def get_photo_info(self, photo_path: str) -> Optional[dict]:
        """
        Obtém informações da foto
        
        Args:
            photo_path: Caminho da foto
            
        Returns:
            dict: Informações da foto
        """
        try:
            if not os.path.exists(photo_path):
                return None
            
            with Image.open(photo_path) as img:
                file_size = os.path.getsize(photo_path)
                
                return {
                    'path': photo_path,
                    'filename': os.path.basename(photo_path),
                    'size_bytes': file_size,
                    'size_mb': file_size / (1024 * 1024),
                    'dimensions': img.size,
                    'width': img.width,
                    'height': img.height,
                    'format': img.format,
                    'mode': img.mode,
                    'created_date': datetime.fromtimestamp(os.path.getctime(photo_path)).isoformat(),
                    'modified_date': datetime.fromtimestamp(os.path.getmtime(photo_path)).isoformat()
                }
                
        except Exception as e:
            print(f"❌ Erro ao obter informações da foto: {e}")
            return None
    
    def delete_photo(self, photo_path: str) -> bool:
        """
        Deleta uma foto
        
        Args:
            photo_path: Caminho da foto
            
        Returns:
            bool: True se deletada com sucesso
        """
        try:
            if not os.path.exists(photo_path):
                print(f"⚠️ Foto não encontrada: {photo_path}")
                return False
            
            # Deletar arquivo principal
            os.remove(photo_path)
            
            # Deletar thumbnail se existir
            thumbnail_path = self._get_thumbnail_path(photo_path)
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
            
            print(f"✅ Foto deletada: {photo_path}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao deletar foto: {e}")
            return False
    
    def _get_thumbnail_path(self, photo_path: str) -> str:
        """
        Gera o caminho do thumbnail baseado no caminho da foto
        
        Args:
            photo_path: Caminho da foto
            
        Returns:
            str: Caminho do thumbnail
        """
        dir_path = os.path.dirname(photo_path)
        filename = os.path.basename(photo_path)
        name, ext = os.path.splitext(filename)
        thumbnail_name = f"{name}_thumb{ext}"
        return os.path.join(dir_path, thumbnail_name)
    
    def copy_photo_to_inspection(self, photo_path: str, inspection_id: int) -> Optional[str]:
        """
        Copia foto para pasta específica da inspeção
        
        Args:
            photo_path: Caminho da foto original
            inspection_id: ID da inspeção
            
        Returns:
            str: Caminho da foto copiada
        """
        try:
            # Criar pasta da inspeção
            inspection_dir = os.path.join(self.photos_dir, f"inspecao_{inspection_id}")
            if not os.path.exists(inspection_dir):
                os.makedirs(inspection_dir)
            
            # Copiar foto
            filename = os.path.basename(photo_path)
            new_path = os.path.join(inspection_dir, filename)
            shutil.copy2(photo_path, new_path)
            
            print(f"✅ Foto copiada para inspeção: {new_path}")
            return new_path
            
        except Exception as e:
            print(f"❌ Erro ao copiar foto: {e}")
            return None
    
    def get_all_photos(self) -> List[str]:
        """
        Retorna todas as fotos armazenadas
        
        Returns:
            List[str]: Lista de caminhos das fotos
        """
        try:
            photos = []
            for root, dirs, files in os.walk(self.photos_dir):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in self.supported_formats):
                        photos.append(os.path.join(root, file))
            
            return photos
            
        except Exception as e:
            print(f"❌ Erro ao listar fotos: {e}")
            return []
    
    def cleanup_orphaned_photos(self) -> int:
        """
        Remove fotos órfãs (sem referência no banco)
        
        Returns:
            int: Número de fotos removidas
        """
        try:
            # Esta função seria chamada com uma lista de fotos válidas do banco
            # Por enquanto, apenas retorna 0
            return 0
            
        except Exception as e:
            print(f"❌ Erro ao limpar fotos órfãs: {e}")
            return 0

class PhotoPreview:
    """Classe para preview de fotos na interface"""
    
    def __init__(self, parent_widget, max_size: Tuple[int, int] = (300, 300)):
        """
        Inicializa o preview de foto
        
        Args:
            parent_widget: Widget pai para exibir a foto
            max_size: Tamanho máximo do preview
        """
        self.parent_widget = parent_widget
        self.max_size = max_size
        self.current_photo = None
        self.photo_label = None
        
        self._create_photo_label()
    
    def _create_photo_label(self):
        """Cria o label para exibir a foto"""
        self.photo_label = tk.Label(self.parent_widget, text="Nenhuma foto selecionada")
        self.photo_label.pack(pady=10)
    
    def update_preview(self, photo_path: str):
        """
        Atualiza o preview com uma nova foto
        
        Args:
            photo_path: Caminho da foto
        """
        try:
            if not photo_path or not os.path.exists(photo_path):
                self.clear_preview()
                return
            
            # Abrir e redimensionar imagem
            with Image.open(photo_path) as img:
                # Manter proporção
                img.thumbnail(self.max_size, Image.Resampling.LANCZOS)
                
                # Converter para PhotoImage
                photo = ImageTk.PhotoImage(img)
                
                # Atualizar label
                self.photo_label.configure(image=photo, text="")
                self.photo_label.image = photo  # Manter referência
                
                self.current_photo = photo_path
                
        except Exception as e:
            print(f"❌ Erro ao atualizar preview: {e}")
            self.photo_label.configure(text=f"Erro ao carregar foto: {e}")
    
    def clear_preview(self):
        """Limpa o preview"""
        self.photo_label.configure(image="", text="Nenhuma foto selecionada")
        self.current_photo = None
    
    def get_current_photo(self) -> Optional[str]:
        """
        Retorna o caminho da foto atual
        
        Returns:
            str: Caminho da foto ou None
        """
        return self.current_photo

# Funções de conveniência para compatibilidade com o React
def handle_photo_upload(photo_path: str) -> Optional[str]:
    """
    Manipula upload de foto (equivalente ao handleChange do React)
    
    Args:
        photo_path: Caminho da foto selecionada
        
    Returns:
        str: Caminho da foto processada ou None
    """
    handler = PhotoHandler()
    return handler.validate_and_process_photo(photo_path)

def create_photo_preview(parent_widget, max_size: Tuple[int, int] = (300, 300)) -> PhotoPreview:
    """
    Cria um preview de foto (equivalente ao previewFoto do React)
    
    Args:
        parent_widget: Widget pai
        max_size: Tamanho máximo
        
    Returns:
        PhotoPreview: Objeto de preview
    """
    return PhotoPreview(parent_widget, max_size)

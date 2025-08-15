# -*- coding: utf-8 -*-
"""
Sistema de geração de relatórios PDF para inspeções
Substitui o gerarPdfInspecao do React
"""

import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

class InspectionReportGenerator:
    """Classe para gerar relatórios de inspeção em PDF"""
    
    def __init__(self, output_dir: str = 'relatorios'):
        """
        Inicializa o gerador de relatórios
        
        Args:
            output_dir: Diretório para salvar os relatórios
        """
        self.output_dir = output_dir
        self.styles = getSampleStyleSheet()
        self._ensure_output_directory()
        self._setup_custom_styles()
    
    def _ensure_output_directory(self):
        """Garante que o diretório de saída existe"""
        try:
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
                print(f"✅ Diretório de relatórios criado: {self.output_dir}")
        except Exception as e:
            print(f"❌ Erro ao criar diretório de relatórios: {e}")
            raise
    
    def _setup_custom_styles(self):
        """Configura estilos personalizados para o relatório"""
        # Título principal
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        # Subtítulos
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            spaceBefore=20,
            textColor=colors.darkgreen
        )
        
        # Cabeçalhos de seção
        self.section_style = ParagraphStyle(
            'CustomSection',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceAfter=15,
            spaceBefore=15,
            textColor=colors.black
        )
        
        # Texto normal
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6
        )
        
        # Texto pequeno
        self.small_style = ParagraphStyle(
            'CustomSmall',
            parent=self.styles['Normal'],
            fontSize=8,
            spaceAfter=4
        )
    
    def generate_inspection_report(self, inspection_data: Dict[str, Any], 
                                 photo_path: Optional[str] = None) -> str:
        """
        Gera relatório individual de inspeção
        
        Args:
            inspection_data: Dados da inspeção
            photo_path: Caminho da foto (opcional)
            
        Returns:
            str: Caminho do arquivo PDF gerado
        """
        try:
            # Gerar nome do arquivo
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            equipment_tag = inspection_data.get('tag', 'UNKNOWN')
            filename = f"relatorio_inspecao_{equipment_tag}_{timestamp}.pdf"
            filepath = os.path.join(self.output_dir, filename)
            
            # Criar documento
            doc = SimpleDocTemplate(filepath, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm,
                                 topMargin=2*cm, bottomMargin=2*cm)
            
            # Conteúdo do relatório
            story = []
            
            # Título
            story.append(Paragraph("RELATÓRIO DE INSPEÇÃO DE EQUIPAMENTO", self.title_style))
            story.append(Spacer(1, 20))
            
            # Informações básicas
            story.extend(self._create_basic_info_section(inspection_data))
            story.append(Spacer(1, 20))
            
            # Detalhes da inspeção
            story.extend(self._create_inspection_details_section(inspection_data))
            story.append(Spacer(1, 20))
            
            # Foto (se fornecida)
            if photo_path and os.path.exists(photo_path):
                story.extend(self._create_photo_section(photo_path))
                story.append(Spacer(1, 20))
            
            # Status e recomendações
            story.extend(self._create_status_section(inspection_data))
            story.append(Spacer(1, 20))
            
            # Rodapé
            story.extend(self._create_footer_section())
            
            # Construir PDF
            doc.build(story)
            
            print(f"✅ Relatório gerado: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Erro ao gerar relatório: {e}")
            raise
    
    def _create_basic_info_section(self, data: Dict[str, Any]) -> List[Flowable]:
        """Cria seção de informações básicas"""
        elements = []
        
        elements.append(Paragraph("INFORMAÇÕES BÁSICAS", self.subtitle_style))
        
        # Tabela de informações
        basic_info = [
            ['Campo', 'Valor'],
            ['Plataforma', data.get('plataforma', 'N/A')],
            ['Módulo', data.get('modulo', 'N/A')],
            ['Setor', data.get('setor', 'N/A')],
            ['Tipo de Equipamento', data.get('tipoEquipamento', 'N/A')],
            ['TAG', data.get('tag', 'N/A')]
        ]
        
        table = Table(basic_info, colWidths=[3*cm, 8*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        return elements
    
    def _create_inspection_details_section(self, data: Dict[str, Any]) -> List[Flowable]:
        """Cria seção de detalhes da inspeção"""
        elements = []
        
        elements.append(Paragraph("DETALHES DA INSPEÇÃO", self.subtitle_style))
        
        # Tabela de detalhes
        inspection_details = [
            ['Campo', 'Valor'],
            ['Data da Última Inspeção', data.get('ultima', 'N/A')],
            ['Data da Inspeção Atual', data.get('data', 'N/A')],
            ['Tipo de Dano', data.get('tipoDano', 'N/A')],
            ['Defeito Identificado', data.get('defeito', 'N/A')],
            ['Causa do Defeito', data.get('causa', 'N/A')],
            ['Categoria RTI', data.get('categoriaRTI', 'N/A')],
            ['Recomendação', data.get('recomendacao', 'N/A')]
        ]
        
        table = Table(inspection_details, colWidths=[4*cm, 7*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        
        # Observações
        if data.get('observacoes'):
            elements.append(Spacer(1, 15))
            elements.append(Paragraph("OBSERVAÇÕES:", self.section_style))
            elements.append(Paragraph(data['observacoes'], self.normal_style))
        
        return elements
    
    def _create_photo_section(self, photo_path: str) -> List[Flowable]:
        """Cria seção da foto"""
        elements = []
        
        elements.append(Paragraph("FOTO DA INSPEÇÃO", self.subtitle_style))
        
        try:
            # Redimensionar imagem para o PDF
            img = Image(photo_path, width=6*cm, height=4*cm)
            elements.append(img)
            
            # Informações da foto
            photo_info = f"Arquivo: {os.path.basename(photo_path)}"
            elements.append(Paragraph(photo_info, self.small_style))
            
        except Exception as e:
            elements.append(Paragraph(f"Erro ao carregar foto: {e}", self.normal_style))
        
        return elements
    
    def _create_status_section(self, data: Dict[str, Any]) -> List[Flowable]:
        """Cria seção de status e recomendações"""
        elements = []
        
        elements.append(Paragraph("STATUS E RECOMENDAÇÕES", self.subtitle_style))
        
        # Calcular status da inspeção
        from date_validator import DateValidator
        
        last_inspection = data.get('ultima', '')
        if last_inspection:
            status_info = DateValidator.get_inspection_status(last_inspection, 12)
            
            # Tabela de status
            status_data = [
                ['Status', 'Descrição'],
                ['Última Inspeção', status_info.get('last_inspection_formatted', 'N/A')],
                ['Próxima Inspeção', status_info.get('next_inspection_formatted', 'N/A')],
                ['Dias até Vencimento', str(status_info.get('days_until_due', 'N/A'))],
                ['Mensagem', status_info.get('message', 'N/A')]
            ]
            
            table = Table(status_data, colWidths=[4*cm, 7*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(table)
        
        return elements
    
    def _create_footer_section(self) -> List[Flowable]:
        """Cria seção do rodapé"""
        elements = []
        
        elements.append(Spacer(1, 30))
        elements.append(Paragraph("_" * 50, self.normal_style))
        
        # Informações de geração
        generation_info = f"Relatório gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}"
        elements.append(Paragraph(generation_info, self.small_style))
        
        elements.append(Paragraph("Sistema de Inspeção de Equipamentos", self.small_style))
        
        return elements
    
    def generate_batch_reports(self, inspections: List[Dict[str, Any]]) -> List[str]:
        """
        Gera relatórios em lote para múltiplas inspeções
        
        Args:
            inspections: Lista de inspeções
            
        Returns:
            List[str]: Lista de caminhos dos PDFs gerados
        """
        generated_files = []
        
        try:
            print(f"🔄 Gerando {len(inspections)} relatórios em lote...")
            
            for i, inspection in enumerate(inspections, 1):
                try:
                    # Buscar foto se existir
                    photo_path = inspection.get('foto_path')
                    
                    # Gerar relatório
                    pdf_path = self.generate_inspection_report(inspection, photo_path)
                    generated_files.append(pdf_path)
                    
                    print(f"✅ Relatório {i}/{len(inspections)} gerado: {os.path.basename(pdf_path)}")
                    
                except Exception as e:
                    print(f"❌ Erro ao gerar relatório {i}: {e}")
                    continue
            
            print(f"🎉 Geração em lote concluída: {len(generated_files)}/{len(inspections)} relatórios")
            return generated_files
            
        except Exception as e:
            print(f"❌ Erro na geração em lote: {e}")
            return generated_files
    
    def generate_summary_report(self, inspections: List[Dict[str, Any]]) -> str:
        """
        Gera relatório resumo de todas as inspeções
        
        Args:
            inspections: Lista de inspeções
            
        Returns:
            str: Caminho do PDF resumo
        """
        try:
            # Gerar nome do arquivo
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"relatorio_resumo_inspecoes_{timestamp}.pdf"
            filepath = os.path.join(self.output_dir, filename)
            
            # Criar documento
            doc = SimpleDocTemplate(filepath, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm,
                                 topMargin=2*cm, bottomMargin=2*cm)
            
            # Conteúdo do resumo
            story = []
            
            # Título
            story.append(Paragraph("RELATÓRIO RESUMO DE INSPEÇÕES", self.title_style))
            story.append(Spacer(1, 20))
            
            # Estatísticas gerais
            story.extend(self._create_summary_statistics(inspections))
            story.append(Spacer(1, 20))
            
            # Tabela resumo
            story.extend(self._create_summary_table(inspections))
            story.append(Spacer(1, 20))
            
            # Rodapé
            story.extend(self._create_footer_section())
            
            # Construir PDF
            doc.build(story)
            
            print(f"✅ Relatório resumo gerado: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Erro ao gerar relatório resumo: {e}")
            raise
    
    def _create_summary_statistics(self, inspections: List[Dict[str, Any]]) -> List[Flowable]:
        """Cria estatísticas do resumo"""
        elements = []
        
        elements.append(Paragraph("ESTATÍSTICAS GERAIS", self.subtitle_style))
        
        # Calcular estatísticas
        total_inspections = len(inspections)
        equipment_types = {}
        platforms = {}
        overdue_count = 0
        
        from date_validator import DateValidator
        
        for inspection in inspections:
            # Contar tipos de equipamento
            eq_type = inspection.get('tipoEquipamento', 'N/A')
            equipment_types[eq_type] = equipment_types.get(eq_type, 0) + 1
            
            # Contar plataformas
            platform = inspection.get('plataforma', 'N/A')
            platforms[platform] = platforms.get(platform, 0) + 1
            
            # Contar vencidas
            last_inspection = inspection.get('ultima', '')
            if last_inspection and DateValidator.is_overdue(last_inspection, 12):
                overdue_count += 1
        
        # Criar tabela de estatísticas
        stats_data = [
            ['Métrica', 'Valor'],
            ['Total de Inspeções', str(total_inspections)],
            ['Inspeções Vencidas', str(overdue_count)],
            ['Inspeções em Dia', str(total_inspections - overdue_count)]
        ]
        
        table = Table(stats_data, colWidths=[4*cm, 7*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        return elements
    
    def _create_summary_table(self, inspections: List[Dict[str, Any]]) -> List[Flowable]:
        """Cria tabela resumo das inspeções"""
        elements = []
        
        elements.append(Paragraph("RESUMO DAS INSPEÇÕES", self.subtitle_style))
        
        # Preparar dados da tabela
        table_data = [['TAG', 'Tipo', 'Plataforma', 'Última Inspeção', 'Status']]
        
        from date_validator import DateValidator
        
        for inspection in inspections:
            tag = inspection.get('tag', 'N/A')
            eq_type = inspection.get('tipoEquipamento', 'N/A')
            platform = inspection.get('plataforma', 'N/A')
            last_inspection = inspection.get('ultima', 'N/A')
            
            # Determinar status
            if last_inspection != 'N/A':
                status_info = DateValidator.get_inspection_status(last_inspection, 12)
                status = status_info.get('message', 'N/A')
            else:
                status = 'N/A'
            
            table_data.append([tag, eq_type, platform, last_inspection, status])
        
        # Criar tabela
        table = Table(table_data, colWidths=[2*cm, 3*cm, 2*cm, 3*cm, 4*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        return elements

# Funções de conveniência para compatibilidade com o React
def gerar_pdf_inspecao(inspection_data: Dict[str, Any], photo_path: Optional[str] = None) -> str:
    """
    Gera PDF de inspeção (equivalente ao gerarPdfInspecao do React)
    
    Args:
        inspection_data: Dados da inspeção
        photo_path: Caminho da foto (opcional)
        
    Returns:
        str: Caminho do PDF gerado
    """
    generator = InspectionReportGenerator()
    return generator.generate_inspection_report(inspection_data, photo_path)

def gerar_relatorios_lote(inspections: List[Dict[str, Any]]) -> List[str]:
    """
    Gera relatórios em lote (equivalente ao batch do React)
    
    Args:
        inspections: Lista de inspeções
        
    Returns:
        List[str]: Lista de PDFs gerados
    """
    generator = InspectionReportGenerator()
    return generator.generate_batch_reports(inspections)

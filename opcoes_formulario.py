# -*- coding: utf-8 -*-
"""
Opções do formulário de inspeção
Baseado no projeto React original
"""

# Opções para os campos do formulário
OPCOES_FORMULARIO = {
    'plataforma': ['P-1', 'P-2', 'P-3', 'P-4'],
    'modulo': ['M01', 'M02', 'M03', 'M04', 'M05', 'M06', 'M07', 'M08', 'M09', 'M10'],
    'setor': ['S01', 'S02', 'S03'],
    'tipoEquipamento': ['Vaso de Pressão', 'Tanque', 'Permutador', 'Filtro'],
    'tag': {
        'Vaso de Pressão': [f'VP-{str(i+1).zfill(3)}' for i in range(50)],
        'Tanque': [f'TQ-{str(i+1).zfill(3)}' for i in range(40)],
        'Permutador': [f'PM-{str(i+1).zfill(3)}' for i in range(30)],
        'Filtro': [f'FT-{str(i+1).zfill(3)}' for i in range(100)],
    },
    'defeito': ['Redução de espessura', 'Vazamento', 'Trinca', 'Desgaste anormal', 'Outro'],
    'causa': ['Corrosão externa', 'Corrosão interna', 'Vibração excessiva', 'Impacto', 'Outro'],
    'categoriaRTI': ['I', 'II', 'III', 'IV'],
    'recomendacao': ['Reparar imediatamente', 'Estender prazo de execução', 'Interromper o serviço', 'Pintura', 'Outra'],
    'tipoDano': ['Localizado', 'Disperso', 'Generalizado']
}

# Estado inicial do formulário
ESTADO_INICIAL = {
    'plataforma': '',
    'modulo': '',
    'setor': '',
    'tipoEquipamento': '',
    'tag': '',
    'defeito': '',
    'causa': '',
    'categoriaRTI': '',
    'recomendacao': '',
    'ultima': '',
    'data': '',
    'tipoDano': '',
    'observacoes': '',
    'foto': None
}

def get_tags_por_tipo(tipo_equipamento):
    """Retorna as tags disponíveis para um tipo de equipamento"""
    return OPCOES_FORMULARIO['tag'].get(tipo_equipamento, [])

def get_todas_opcoes():
    """Retorna todas as opções do formulário"""
    return OPCOES_FORMULARIO

def get_estado_inicial():
    """Retorna o estado inicial do formulário"""
    return ESTADO_INICIAL.copy()

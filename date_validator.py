# -*- coding: utf-8 -*-
"""
Sistema de validação de datas para inspeções
Baseado no projeto React original
"""

from datetime import datetime, timedelta
from typing import Tuple, Optional
import calendar

class DateValidator:
    """Classe para validação e manipulação de datas"""
    
    @staticmethod
    def validate_inspection_date(date_str: str) -> Tuple[bool, str]:
        """
        Valida uma data de inspeção
        
        Args:
            date_str: Data no formato 'YYYY-MM-DD'
            
        Returns:
            Tuple[bool, str]: (é_válida, mensagem)
        """
        try:
            if not date_str:
                return False, "Data de inspeção é obrigatória"
            
            inspection_date = datetime.strptime(date_str, '%Y-%m-%d')
            today = datetime.now().date()
            
            if inspection_date.date() > today:
                return False, "Data de inspeção não pode ser no futuro"
            
            if inspection_date.date() < today - timedelta(days=30):
                return False, "Data de inspeção não pode ser há mais de 30 dias"
            
            return True, "Data válida"
            
        except ValueError:
            return False, "Formato de data inválido. Use YYYY-MM-DD"
    
    @staticmethod
    def validate_last_inspection_date(date_str: str) -> Tuple[bool, str]:
        """
        Valida a data da última inspeção
        
        Args:
            date_str: Data no formato 'YYYY-MM-DD'
            
        Returns:
            Tuple[bool, str]: (é_válida, mensagem)
        """
        try:
            if not date_str:
                return False, "Data da última inspeção é obrigatória"
            
            last_date = datetime.strptime(date_str, '%Y-%m-%d')
            today = datetime.now().date()
            
            if last_date.date() > today:
                return False, "Data da última inspeção não pode ser no futuro"
            
            if last_date.date() < today - timedelta(days=3650):  # 10 anos
                return False, "Data da última inspeção não pode ser há mais de 10 anos"
            
            return True, "Data válida"
            
        except ValueError:
            return False, "Formato de data inválido. Use YYYY-MM-DD"
    
    @staticmethod
    def calculate_next_inspection_date(last_inspection_date: str, validity_months: int = 12) -> str:
        """
        Calcula a data da próxima inspeção baseada na validade
        
        Args:
            last_inspection_date: Data da última inspeção (YYYY-MM-DD)
            validity_months: Meses de validade (padrão: 12)
            
        Returns:
            str: Data da próxima inspeção (YYYY-MM-DD)
        """
        try:
            last_date = datetime.strptime(last_inspection_date, '%Y-%m-%d')
            next_date = last_date + timedelta(days=validity_months * 30)
            return next_date.strftime('%Y-%m-%d')
        except ValueError:
            return ""
    
    @staticmethod
    def is_overdue(last_inspection_date: str, validity_months: int = 12) -> bool:
        """
        Verifica se a inspeção está vencida
        
        Args:
            last_inspection_date: Data da última inspeção (YYYY-MM-DD)
            validity_months: Meses de validade (padrão: 12)
            
        Returns:
            bool: True se estiver vencida
        """
        try:
            if not last_inspection_date:
                return False
            
            last_date = datetime.strptime(last_inspection_date, '%Y-%m-%d')
            due_date = last_date + timedelta(days=validity_months * 30)
            today = datetime.now().date()
            
            return today > due_date.date()
            
        except ValueError:
            return False
    
    @staticmethod
    def get_days_until_due(last_inspection_date: str, validity_months: int = 12) -> int:
        """
        Calcula quantos dias faltam até o vencimento
        
        Args:
            last_inspection_date: Data da última inspeção (YYYY-MM-DD)
            validity_months: Meses de validade (padrão: 12)
            
        Returns:
            int: Dias até o vencimento (negativo se vencida)
        """
        try:
            if not last_inspection_date:
                return 0
            
            last_date = datetime.strptime(last_inspection_date, '%Y-%m-%d')
            due_date = last_date + timedelta(days=validity_months * 30)
            today = datetime.now().date()
            
            delta = due_date.date() - today
            return delta.days
            
        except ValueError:
            return 0
    
    @staticmethod
    def format_date_for_display(date_str: str, format_type: str = 'short') -> str:
        """
        Formata data para exibição
        
        Args:
            date_str: Data no formato 'YYYY-MM-DD'
            format_type: Tipo de formatação ('short', 'long', 'relative')
            
        Returns:
            str: Data formatada
        """
        try:
            if not date_str:
                return ""
            
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            today = datetime.now().date()
            
            if format_type == 'short':
                return date_obj.strftime('%d/%m/%Y')
            elif format_type == 'long':
                return date_obj.strftime('%d de %B de %Y')
            elif format_type == 'relative':
                delta = today - date_obj.date()
                if delta.days == 0:
                    return "Hoje"
                elif delta.days == 1:
                    return "Ontem"
                elif delta.days == -1:
                    return "Amanhã"
                elif delta.days > 0:
                    return f"Há {delta.days} dias"
                else:
                    return f"Em {abs(delta.days)} dias"
            else:
                return date_obj.strftime('%d/%m/%Y')
                
        except ValueError:
            return date_str
    
    @staticmethod
    def get_inspection_status(last_inspection_date: str, validity_months: int = 12) -> dict:
        """
        Retorna o status completo da inspeção
        
        Args:
            last_inspection_date: Data da última inspeção (YYYY-MM-DD)
            validity_months: Meses de validade (padrão: 12)
            
        Returns:
            dict: Status da inspeção
        """
        try:
            if not last_inspection_date:
                return {
                    'status': 'unknown',
                    'message': 'Data não informada',
                    'is_overdue': False,
                    'days_until_due': 0,
                    'next_inspection_date': '',
                    'last_inspection_formatted': ''
                }
            
            last_date = datetime.strptime(last_inspection_date, '%Y-%m-%d')
            next_date = last_date + timedelta(days=validity_months * 30)
            today = datetime.now().date()
            days_until_due = (next_date.date() - today).days
            
            # Determinar status
            if days_until_due < 0:
                status = 'overdue'
                message = 'Inspeção vencida!'
            elif days_until_due <= 30:
                status = 'warning'
                message = 'Inspeção vence em breve'
            elif days_until_due <= 90:
                status = 'attention'
                message = 'Inspeção vence em alguns meses'
            else:
                status = 'ok'
                message = 'Inspeção em dia'
            
            return {
                'status': status,
                'message': message,
                'is_overdue': days_until_due < 0,
                'days_until_due': days_until_due,
                'next_inspection_date': next_date.strftime('%Y-%m-%d'),
                'next_inspection_formatted': next_date.strftime('%d/%m/%Y'),
                'last_inspection_formatted': last_date.strftime('%d/%m/%Y'),
                'last_inspection_date': last_inspection_date
            }
            
        except ValueError:
            return {
                'status': 'error',
                'message': 'Erro ao processar data',
                'is_overdue': False,
                'days_until_due': 0,
                'next_inspection_date': '',
                'last_inspection_formatted': ''
            }
    
    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, str]:
        """
        Valida um intervalo de datas
        
        Args:
            start_date: Data inicial (YYYY-MM-DD)
            end_date: Data final (YYYY-MM-DD)
            
        Returns:
            Tuple[bool, str]: (é_válido, mensagem)
        """
        try:
            if not start_date or not end_date:
                return False, "Ambas as datas são obrigatórias"
            
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            if start > end:
                return False, "Data inicial não pode ser posterior à data final"
            
            if (end - start).days > 365:
                return False, "Intervalo não pode ser maior que 1 ano"
            
            return True, "Intervalo válido"
            
        except ValueError:
            return False, "Formato de data inválido. Use YYYY-MM-DD"
    
    @staticmethod
    def get_monthly_inspection_dates(year: int, month: int) -> list:
        """
        Retorna todas as datas de inspeção de um mês específico
        
        Args:
            year: Ano
            month: Mês (1-12)
            
        Returns:
            list: Lista de datas de inspeção
        """
        try:
            # Primeiro dia do mês
            first_day = datetime(year, month, 1)
            
            # Último dia do mês
            if month == 12:
                last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                last_day = datetime(year, month + 1, 1) - timedelta(days=1)
            
            # Gerar todas as datas do mês
            dates = []
            current = first_day
            while current <= last_day:
                dates.append(current.strftime('%Y-%m-%d'))
                current += timedelta(days=1)
            
            return dates
            
        except ValueError:
            return []
    
    @staticmethod
    def get_working_days_between(start_date: str, end_date: str) -> int:
        """
        Calcula o número de dias úteis entre duas datas
        
        Args:
            start_date: Data inicial (YYYY-MM-DD)
            end_date: Data final (YYYY-MM-DD)
            
        Returns:
            int: Número de dias úteis
        """
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            working_days = 0
            current = start
            
            while current <= end:
                if current.weekday() < 5:  # Segunda a Sexta
                    working_days += 1
                current += timedelta(days=1)
            
            return working_days
            
        except ValueError:
            return 0

# Funções de conveniência para compatibilidade com o React
def is_vencido(ultima_inspecao: str) -> bool:
    """
    Verifica se a inspeção está vencida (equivalente ao isVencido do React)
    
    Args:
        ultima_inspecao: Data da última inspeção (YYYY-MM-DD)
        
    Returns:
        bool: True se estiver vencida
    """
    return DateValidator.is_overdue(ultima_inspecao, 12)

def add_days(date_str: str, days: int) -> str:
    """
    Adiciona dias a uma data (equivalente ao addDays do React)
    
    Args:
        date_str: Data inicial (YYYY-MM-DD)
        days: Número de dias a adicionar
        
    Returns:
        str: Nova data (YYYY-MM-DD)
    """
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        new_date = date_obj + timedelta(days=days)
        return new_date.strftime('%Y-%m-%d')
    except ValueError:
        return date_str

def format_date(date_str: str) -> str:
    """
    Formata data para exibição (equivalente ao format do React)
    
    Args:
        date_str: Data (YYYY-MM-DD)
        
    Returns:
        str: Data formatada (dd/MM/yyyy)
    """
    return DateValidator.format_date_for_display(date_str, 'short')

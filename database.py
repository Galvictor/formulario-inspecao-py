# -*- coding: utf-8 -*-
"""
Sistema de banco de dados para inspeções
Substitui o IndexedDB do React por SQLite
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

class InspectionDatabase:
    """Classe para gerenciar o banco de dados de inspeções"""
    
    def __init__(self, db_path: str = 'inspecoes.db'):
        """Inicializa o banco de dados"""
        self.db_path = db_path
        self.conn = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Conecta ao banco de dados"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            # Habilitar foreign keys
            self.conn.execute("PRAGMA foreign_keys = ON")
            # Configurar para retornar dicionários
            self.conn.row_factory = sqlite3.Row
            print(f"✅ Conectado ao banco: {self.db_path}")
        except Exception as e:
            print(f"❌ Erro ao conectar ao banco: {e}")
            raise
    
    def create_tables(self):
        """Cria as tabelas necessárias"""
        try:
            cursor = self.conn.cursor()
            
            # Tabela principal de inspeções
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inspecoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plataforma TEXT NOT NULL,
                    modulo TEXT NOT NULL,
                    setor TEXT NOT NULL,
                    tipo_equipamento TEXT NOT NULL,
                    tag TEXT NOT NULL,
                    defeito TEXT NOT NULL,
                    causa TEXT NOT NULL,
                    categoria_rti TEXT NOT NULL,
                    recomendacao TEXT NOT NULL,
                    ultima_inspecao DATE NOT NULL,
                    data_inspecao DATE NOT NULL,
                    tipo_dano TEXT NOT NULL,
                    observacoes TEXT,
                    foto_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela para histórico de alterações
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historico_alteracoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    inspecao_id INTEGER NOT NULL,
                    campo TEXT NOT NULL,
                    valor_anterior TEXT,
                    valor_novo TEXT,
                    data_alteracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (inspecao_id) REFERENCES inspecoes (id)
                )
            ''')
            
            # Índices para melhor performance
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_inspecoes_tag ON inspecoes(tag)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_inspecoes_data ON inspecoes(data_inspecao)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_inspecoes_plataforma ON inspecoes(plataforma)
            ''')
            
            self.conn.commit()
            print("✅ Tabelas criadas com sucesso")
            
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
            raise
    
    def save_inspection(self, data: Dict[str, Any]) -> int:
        """Salva uma nova inspeção"""
        try:
            cursor = self.conn.cursor()
            
            # Preparar dados para inserção
            inspection_data = (
                data.get('plataforma', ''),
                data.get('modulo', ''),
                data.get('setor', ''),
                data.get('tipoEquipamento', ''),
                data.get('tag', ''),
                data.get('defeito', ''),
                data.get('causa', ''),
                data.get('categoriaRTI', ''),
                data.get('recomendacao', ''),
                data.get('ultima', ''),
                data.get('data', ''),
                data.get('tipoDano', ''),
                data.get('observacoes', ''),
                data.get('foto_path', ''),
                datetime.now().isoformat(),
                datetime.now().isoformat()
            )
            
            cursor.execute('''
                INSERT INTO inspecoes (
                    plataforma, modulo, setor, tipo_equipamento, tag, defeito, causa,
                    categoria_rti, recomendacao, ultima_inspecao, data_inspecao,
                    tipo_dano, observacoes, foto_path, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', inspection_data)
            
            inspection_id = cursor.lastrowid
            self.conn.commit()
            
            print(f"✅ Inspeção salva com ID: {inspection_id}")
            return inspection_id
            
        except Exception as e:
            print(f"❌ Erro ao salvar inspeção: {e}")
            self.conn.rollback()
            raise
    
    def get_all_inspections(self) -> List[Dict[str, Any]]:
        """Retorna todas as inspeções"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM inspecoes 
                ORDER BY data_inspecao DESC, created_at DESC
            ''')
            
            inspections = []
            for row in cursor.fetchall():
                inspection = dict(row)
                inspections.append(inspection)
            
            print(f"✅ {len(inspections)} inspeções encontradas")
            return inspections
            
        except Exception as e:
            print(f"❌ Erro ao buscar inspeções: {e}")
            return []
    
    def get_inspection_by_id(self, inspection_id: int) -> Optional[Dict[str, Any]]:
        """Retorna uma inspeção específica por ID"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM inspecoes WHERE id = ?', (inspection_id,))
            
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
            
        except Exception as e:
            print(f"❌ Erro ao buscar inspeção {inspection_id}: {e}")
            return None
    
    def update_inspection(self, inspection_id: int, data: Dict[str, Any]) -> bool:
        """Atualiza uma inspeção existente"""
        try:
            cursor = self.conn.cursor()
            
            # Buscar dados atuais para histórico
            current_data = self.get_inspection_by_id(inspection_id)
            if not current_data:
                return False
            
            # Preparar dados para atualização
            update_data = (
                data.get('plataforma', ''),
                data.get('modulo', ''),
                data.get('setor', ''),
                data.get('tipoEquipamento', ''),
                data.get('tag', ''),
                data.get('defeito', ''),
                data.get('causa', ''),
                data.get('categoriaRTI', ''),
                data.get('recomendacao', ''),
                data.get('ultima', ''),
                data.get('data', ''),
                data.get('tipoDano', ''),
                data.get('observacoes', ''),
                data.get('foto_path', ''),
                datetime.now().isoformat(),
                inspection_id
            )
            
            cursor.execute('''
                UPDATE inspecoes SET
                    plataforma = ?, modulo = ?, setor = ?, tipo_equipamento = ?,
                    tag = ?, defeito = ?, causa = ?, categoria_rti = ?,
                    recomendacao = ?, ultima_inspecao = ?, data_inspecao = ?,
                    tipo_dano = ?, observacoes = ?, foto_path = ?, updated_at = ?
                WHERE id = ?
            ''', update_data)
            
            # Registrar alterações no histórico
            self._log_changes(inspection_id, current_data, data)
            
            self.conn.commit()
            print(f"✅ Inspeção {inspection_id} atualizada com sucesso")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao atualizar inspeção {inspection_id}: {e}")
            self.conn.rollback()
            return False
    
    def delete_inspection(self, inspection_id: int) -> bool:
        """Deleta uma inspeção"""
        try:
            cursor = self.conn.cursor()
            
            # Buscar caminho da foto para deletar arquivo
            inspection = self.get_inspection_by_id(inspection_id)
            if inspection and inspection.get('foto_path'):
                try:
                    if os.path.exists(inspection['foto_path']):
                        os.remove(inspection['foto_path'])
                        print(f"✅ Foto removida: {inspection['foto_path']}")
                except Exception as e:
                    print(f"⚠️ Erro ao remover foto: {e}")
            
            cursor.execute('DELETE FROM inspecoes WHERE id = ?', (inspection_id,))
            self.conn.commit()
            
            print(f"✅ Inspeção {inspection_id} deletada com sucesso")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao deletar inspeção {inspection_id}: {e}")
            self.conn.rollback()
            return False
    
    def clear_all_inspections(self) -> bool:
        """Remove todas as inspeções"""
        try:
            cursor = self.conn.cursor()
            
            # Remover todas as fotos
            cursor.execute('SELECT foto_path FROM inspecoes WHERE foto_path IS NOT NULL')
            for row in cursor.fetchall():
                foto_path = row['foto_path']
                if foto_path and os.path.exists(foto_path):
                    try:
                        os.remove(foto_path)
                    except Exception as e:
                        print(f"⚠️ Erro ao remover foto: {e}")
            
            cursor.execute('DELETE FROM inspecoes')
            cursor.execute('DELETE FROM historico_alteracoes')
            self.conn.commit()
            
            print("✅ Todas as inspeções foram removidas")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao limpar inspeções: {e}")
            self.conn.rollback()
            return False
    
    def _log_changes(self, inspection_id: int, old_data: Dict, new_data: Dict):
        """Registra alterações no histórico"""
        try:
            cursor = self.conn.cursor()
            
            for field in old_data.keys():
                if field in ['id', 'created_at', 'updated_at']:
                    continue
                    
                old_value = str(old_data.get(field, ''))
                new_value = str(new_data.get(field, ''))
                
                if old_value != new_value:
                    cursor.execute('''
                        INSERT INTO historico_alteracoes 
                        (inspecao_id, campo, valor_anterior, valor_novo)
                        VALUES (?, ?, ?, ?)
                    ''', (inspection_id, field, old_value, new_value))
            
        except Exception as e:
            print(f"⚠️ Erro ao registrar histórico: {e}")
    
    def get_inspections_by_date_range(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Busca inspeções por período"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM inspecoes 
                WHERE data_inspecao BETWEEN ? AND ?
                ORDER BY data_inspecao DESC
            ''', (start_date, end_date))
            
            inspections = []
            for row in cursor.fetchall():
                inspections.append(dict(row))
            
            return inspections
            
        except Exception as e:
            print(f"❌ Erro ao buscar inspeções por período: {e}")
            return []
    
    def get_inspections_by_equipment(self, equipment_type: str) -> List[Dict[str, Any]]:
        """Busca inspeções por tipo de equipamento"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM inspecoes 
                WHERE tipo_equipamento = ?
                ORDER BY data_inspecao DESC
            ''', (equipment_type,))
            
            inspections = []
            for row in cursor.fetchall():
                inspections.append(dict(row))
            
            return inspections
            
        except Exception as e:
            print(f"❌ Erro ao buscar inspeções por equipamento: {e}")
            return []
    
    def close(self):
        """Fecha a conexão com o banco"""
        if self.conn:
            self.conn.close()
            print("✅ Conexão com banco fechada")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

# Funções de conveniência para compatibilidade com o React
def save_data_to_database(data: Dict[str, Any]) -> int:
    """Salva dados no banco (equivalente ao saveDataToIndexedDB do React)"""
    with InspectionDatabase() as db:
        return db.save_inspection(data)

def get_all_inspections() -> List[Dict[str, Any]]:
    """Retorna todas as inspeções (equivalente ao getAllInspecoes do React)"""
    with InspectionDatabase() as db:
        return db.get_all_inspections()

def clear_all_inspections() -> bool:
    """Remove todas as inspeções (equivalente ao clearInspecoes do React)"""
    with InspectionDatabase() as db:
        return db.clear_all_inspections()

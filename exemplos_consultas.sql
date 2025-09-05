-- =============================================
-- EXEMPLOS DE CONSULTAS PARA O BANCO FSA
-- =============================================

-- 1. Ver todos os pacientes
SELECT * FROM paciente;

-- 2. Ver todos os estagiários
SELECT * FROM estagiario;

-- 3. Ver todos os agendamentos
SELECT * FROM agendamento;

-- 4. Contar registros por tabela
SELECT 'Pacientes' as tabela, COUNT(*) as total FROM paciente
UNION ALL
SELECT 'Estagiários' as tabela, COUNT(*) as total FROM estagiario
UNION ALL
SELECT 'Agendamentos' as tabela, COUNT(*) as total FROM agendamento
UNION ALL
SELECT 'Disponibilidades' as tabela, COUNT(*) as total FROM disponibilidade;

-- 5. Ver agendamentos com nomes dos pacientes e estagiários
SELECT 
    a.id,
    p.nome as paciente_nome,
    e.nome as estagiario_nome,
    a.data_solicitacao,
    a.data_agendamento,
    a.status
FROM agendamento a
LEFT JOIN paciente p ON a.paciente_id = p.id
LEFT JOIN estagiario e ON a.estagiario_id = e.id;

-- 6. Pacientes por gênero
SELECT genero, COUNT(*) as total
FROM paciente
GROUP BY genero;

-- 7. Agendamentos por status
SELECT status, COUNT(*) as total
FROM agendamento
GROUP BY status;

-- 8. Estagiários por curso
SELECT curso_periodo, COUNT(*) as total
FROM estagiario
GROUP BY curso_periodo;

-- 9. Buscar paciente por CPF
-- SELECT * FROM paciente WHERE cpf = '12345678901';

-- 10. Buscar agendamentos de um paciente específico
-- SELECT * FROM agendamento WHERE paciente_id = 1;

-- 11. Ver estrutura das tabelas
PRAGMA table_info(paciente);
PRAGMA table_info(estagiario);
PRAGMA table_info(agendamento);
PRAGMA table_info(disponibilidade);


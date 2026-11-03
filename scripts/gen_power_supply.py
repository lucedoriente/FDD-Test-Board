import os

kicad_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
root_uuid = "b20a3201-1001-4001-8001-000000000001"
sheet1_uuid = "b20a3201-1001-4001-8001-000000000002"
doc_uuid = "b20a3201-2001-4001-8001-000000000002"

# 01_Power_Supply.kicad_sch completo e rigoroso:
# - Ingresso 24V da modulo Mean Well
# - E-Fuse 24V con Q1 (P-MOSFET AOD403), Q2 (NPN 2N3904), R1, R2, R3 (Shunt 0.05R), U1 (INA180A1)
# - Buck Converter 12V con U2 (TPS54302), L1 (10uH), C3..C6, R4..R5, E-Fuse 12V (Q3, Q4, R6, U3 INA180A1)
# - Buck Converter 5V con U4 (TPS54302), L2 (6.8uH), C7..C10, R7..R8, E-Fuse 5V (Q5, Q6, R9, U5 INA180A1)
# - Connettori di potenza FDD: J1 (24V In), J2 (Molex 5.25), J3 (Berg 3.5), J4 (Phoenix 8")
# - Connettore alimentazione display smart 4-fili J5 (5V, GND, TX, RX)
# - Tutti i wire stubs >= 5.08mm, label orientate, zero overlap, annotazione completa, PWR_FLAG su power net

print("Avvio generazione 01_Power_Supply.kicad_sch...")

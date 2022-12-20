# imxB_reader.py
Simple code to read Impermax imxB token details. User-level details such as approvals and borrow balances have been left out. Mostly useful for Arbitrum, where source code from factory contracts cannot be verified. 

# Example Usage:
read_imxB('Arbitrum', '0x28D7e687e405538AdFAB80D80069EFA55F09D331') -> returns a CSV file titled 'Arbitrum USDT imxB.csv"

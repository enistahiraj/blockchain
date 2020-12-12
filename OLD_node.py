from blockchain import Blockchain
from uuid import uuid4
from utility.verification import Verification
from wallet import Wallet

class Node:

    def __init__(self):
        #self.wallet.public_key = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

    def get_transaction_value(self):
        """ Returns the input of the user(a new transaction amount) as a float """
        # Get the user input, transform it from a string into a float
        tx_recipient = input('Enter the recipient of the transaction: ')
        tx_amount = float(input('Your transaction amount: '))
        return tx_recipient, tx_amount
        

    def get_user_choice(self):
        """Prompts the user for a choice and return it"""
        user_input = input('Your choice: ')
        return user_input


    def print_blockchain_elements(self):
        """Print all blocks of the blockchain"""
        # output the blockain list to the console
        for block in self.blockchain.chain:
            print('Printing block')
            print(block)


    def listen_for_input(self):
        waiting_for_input = True
        # A while loop for user input interface
        while waiting_for_input:
            print('Please choose: ')
            print('1: Add a Transaction Value')
            print('2: Mine a Block')
            print('3: Print the Blocks')
            print('4: Verify Transactions')
            print('5: Create wallet')
            print('6: Load wallet')
            print('7: Save keys')
            print('q: Quit')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                # add the transaction amount to the blockchain
                signature = self.wallet.sign_transaction(self.wallet.public_key, recipient, amount)
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, signature, amount=amount):
                    print('Added Transaction')
                else:
                    print('Failed Transaction')
                print(self.blockchain.get_open_transaction())
            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print('Mining failed...')
            elif user_choice == '3':
                # call the print function
                self.print_blockchain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transaction(), self.blockchain.get_balance):
                    print('All Transactions are Valid')
                else:
                    print('There are invalid Transactions')
            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '7':
                self.wallet.save_keys()
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print('Input was invalid, please pick one of the choices from the list')
            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print('Invalid blockchain')
                break
            print('Balance of {}: {:6.2f}'.format(self.wallet.public_key, self.blockchain.get_balance()))
        else:
            print('User left')
if __name__ == '__main__':
    node = Node()
    node.listen_for_input()

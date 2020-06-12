# To be installed:
# Flask: pip install Flask
# Postman HTTP Client: https://www.getpostman.com/

#Importing Libraries
import datetime                                         #for time stamp
import hashlib                                          #to hash the blocks
import json                                             #to encode blocks before hashing
from flask import Flask, jsonify                        #web application, to return messages when postman interacts with blockchain

# Section 1: Creating a BlockChain

class Blockchain:
    def __init__(self):                                 #Class always starts with init method with 'self' argument always
        self.chain = []                                 #Initiatilised empty list, Self refers to object after class is made, many objects can be made, var after self will refer to var of object
        self.create_block(proof = 1, previous_hash = '0') 
        
    # Creating a Block
    def create_block(self, proof, previous_hash):
        block = {                                       #{} represents dictionary
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
            }
        self.chain.append(block)                        #add block to the chain
        return block 
    
    # To fetch last block of the chain 
    def get_previous_block(self):
        return self.chain[-1]
    
    #Proof of Work - The number or a piece of data that miners need to find to mine a new block. Hard to find,easy to verify.
    def proof_of_work(self, previous_proof):
        new_proof = 1                                   #Looping variables, needs incrementation
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() # always take non symmetrical operations, encode() for format, haexdigest for hex conversion
            if hash_operation[:4] == '0000':            #Checking for 4 leading zeroes, if satisfied the true else new_proof gets incremented
                check_proof = True
            else:
                new_proof += 1
        return new_proof                                #More the number of leading zeroes, hash harder to find
                  
    #To hash a block
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode() #Use json dumps to make a string, because later blocks will be stored in the format
        return hashlib.sha256(encoded_block).hexdigest()             #sort_keys to sort our blocks by keys
    
    #To check the validity of a Block
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            #Check if previous_hash = hash of previous block
            if block['previous_hash'] != self.hash(previous_block):
                return False
            #Check for proof of work
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            #Moving forward
            previous_block = block
            block_index += 1
        return True
    

# Section 2: Mining our Blockchain

#Creating a Web application
app = Flask(__name__)

#Creating a Blockchain
blockchain = Blockchain() #create an object

#Mining a new Block
@app.route('/mine_block', methods = ['GET'])                   #GET- To get the actual state of blockchain or mining (Get you something), POST- Add a transaction (Creating something)
def mine_block():                                              #No argument because everything will be provided from 'blockchain' object
         previous_block = blockchain.get_previous_block()      #Get the previous block
         previous_proof = previous_block['proof']              #Get proof of the previous block
         proof = blockchain.proof_of_work(previous_proof)      #Proof of new block
         previous_hash = blockchain.hash(previous_block)       #Get the hash of previous_hash
         block = blockchain.create_block(proof, previous_hash) #Create a new block and append it to the Blockchain
         response = {
             'message': 'Congrats, You just mined a block!',
             'index': block['index'],
             'timestamp': block['timestamp'],
             'proof': block['proof'],
             'previous_hash': block['previous_hash']
         }
         return jsonify(response), 200                         #To return the response in the json file, HTTP status code for success is 200

#Getting the full blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,                             #Print chain
        'length': len(blockchain.chain)                        #Print length of the chain
        }
    return jsonify(response), 200

#Check for the validity of the Blockchain
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'Alert message!': 'We have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200
        
#Running the application
app.run(host = '0.0.0.0', port = 5000)                         #Host and port according to Flask


# To Mine a Block: http://127.0.0.1:5000/mine_block
# To Display the Blockchain: http://127.0.0.1:5000/get_chain
# To check for validity: http://127.0.0.1:5000/is_valid
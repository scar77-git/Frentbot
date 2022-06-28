from flask import Flask,render_template
import numpy as np
from flask import Flask, request, jsonify
import pickle
import trax
import json
from trax import layers as tl
from trax.supervised import training
from flask_jsglue import JSGlue


input_text=""
data_dir = 'data'

dialogue_db = {}
vocab_file = "en_32k.subword"
vocab_dir = ''
def tokenize(sentence, vocab_file, vocab_dir):
    return list(trax.data.tokenize(iter([sentence]), vocab_file=vocab_file, vocab_dir=vocab_dir))[0]

def detokenize(tokens, vocab_file, vocab_dir):
    return trax.data.detokenize(tokens, vocab_file=vocab_file, vocab_dir=vocab_dir)
def attention(*args, **kwargs):
    
    kwargs['predict_mem_len'] = 120
    
    kwargs['predict_drop_len'] = 120
    
    return tl.SelfAttention(*args, **kwargs)

def ReformerLM(vocab_size = 33000, n_layers = 6, mode = 'train', attention_type = attention):
  model=  trax.models.reformer.ReformerLM(
      vocab_size = vocab_size,
      n_layers = n_layers,
      mode = mode,
      attention_type = attention_type
  )
  return model



def ReformerLM_output_gen(ReformerLM, start_sentence, vocab_file, vocab_dir, temperature):
    
    
    
    # Create input tokens using the the tokenize function
    input_tokens = tokenize(start_sentence, vocab_file=vocab_file, vocab_dir=vocab_dir)
    
    input_tokens_with_batch = np.array(input_tokens)[None, :]
    
    output_gen = trax.supervised.decoding.autoregressive_sample_stream( 
        # model
        ReformerLM,
        # inputs will be the tokens with batch dimension
        inputs=input_tokens_with_batch,
        # temperature
        temperature=temperature
    )
    
    ### END CODE HERE ###
    
    return output_gen


def generate_dialogue(ReformerLM, model_state, start_sentence, vocab_file, vocab_dir, max_len, temperature):
    
    # define the delimiters we used during training
    delimiter_1 = 'Person 1: ' 
    delimiter_2 = 'Person 2: '
    
    # initialize detokenized output
    sentence = ''
    
    # token counter
    counter = 0
    
    # output tokens. we insert a ': ' for formatting
    result = [tokenize(': ', vocab_file=vocab_file, vocab_dir=vocab_dir)]
    
    # reset the model state when starting a new dialogue
    ReformerLM.state = model_state
    
    # calls the output generator implemented earlier
    output = ReformerLM_output_gen(ReformerLM, start_sentence, vocab_file=vocab_file, vocab_dir = vocab_dir, temperature=temperature)
    
    # print the starting sentence
    #print(start_sentence.split(delimiter_2)[0].strip())
    
    # loop below yields the next tokens until max_len is reached. the if-elif is just for prettifying the output.
    for o in output:
        
        result.append(o)
        
        sentence = detokenize(np.concatenate(result, axis=0), vocab_file=vocab_file, vocab_dir=vocab_dir)
        
        if sentence.endswith(delimiter_1):
            sentence = sentence.split(delimiter_1)[0]
            result.clear()
            return sentence
            #print(f'{delimiter_2}{sentence}')
            #sentence = ''
            #break 

bot_model = ReformerLM(mode ='predict')
app = Flask(__name__)
jsglue = JSGlue(app)

@app.route("/index", methods=['GET','POST'])
def index():
    output=request.get_json()
    input_text = json.loads(output)
    print(input_text)
    #if request.method == "POST":
       
     #  input_text= request.json['inp']
    #return render_template('index.html')

@app.route("/")
def home():
  #STARTING_STATE = bot_model.state
  #shape11 = trax.shapes.ShapeDtype((1, 1), dtype=np.int32)
  #bot_model.init_from_file('chatbot_model1.pkl.gz',
   #                  weights_only=True, input_signature=shape11)
  #STARTING_STATE = bot_model.state
  #result=generate_dialogue(bot_model, model_state=STARTING_STATE, start_sentence=input_text,         vocab_file=vocab_file, vocab_dir=vocab_dir, max_len=120, temperature = 0.2) 
  result="Hello"
  print(input_text)
  return render_template('index.html',result=result)

  
    
app.run()


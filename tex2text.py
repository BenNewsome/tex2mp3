# tex2text.py

# This script parses a latex .tex file and outputs a text file that can then be read by a text-to-speach(tts) engine.

def main(debug=2):

    

    inputs = get_inputs(debug=2)

    tex_input_name = inputs['tex_input_name']

    if (debug>=1): print "tex file name: ", tex_input_name
    output_text = process_file(tex_input_name, debug=2)

    text_output_name = inputs['text_output_name']
    write_text_file(output_text, text_output_name)

    mp3_output_name = inputs['mp3_output_name']
    write_mp3_file(output_text, mp3_output_name, debug=2)

    return;

def write_text_file(output_text, text_output_name):
    
    file = open( text_output_name, 'w')
    file.write(output_text)

    file.close()

    return;

def write_mp3_file(output_text, mp3_output_name, debug=0):

    from gtts import gTTS
    
    if (debug>=1): print "Creating and saving tts output to ", mp3_output_name

    tts = gTTS(text=output_text, lang='en')
    tts.save( mp3_output_name)
    

    return;



def process_file( file_name, debug=0 ):

    special_charicters = create_special_charicters()
    def process_line( line ):
        # This processes a line and removes or replaces any special charicters with its english prenounciation.

        for latex, text in special_charicters.iteritems():
            line = line.replace(latex, text)

        import re
        line = re.sub("\$[^\$]*\$", "", line)

        line = line.replace("\\alttext{", "")
        line = line.replace("}", "")

        return line


    process = process_line

    file = open( file_name, 'r')
    output_text = ""
    figure_text = ""
    
    in_abstract = False
    in_figure   = False


    for line in file:
        tmp_line = ""
        new_line = ""



        if line.startswith( "\\title{" ):
            tmp_line = line.strip()
            new_line = tmp_line[7:-1].strip() + ".\n"
            output_text += process(new_line)
            continue

        if line.startswith( "\\author{" ):
            tmp_line = line.strip()
            new_line = tmp_line[8:-1].strip() + ".\n"
            output_text += process(new_line)
            continue

        if line.startswith( "\\begin{abstract}" ):
            in_abstract=True
            abstract = process(line[16:])
            continue

        if in_abstract:
            tmp_line = line.strip()
            if tmp_line.endswith( "\\end{abstract}" ):
                in_abstract = False
                abstract = abstract + process(tmp_line[:-14]) + "\n"
                output_text = output_text + abstract 
                continue
            else:
                abstract = abstract + process(tmp_line)
                continue

        if line.startswith( "\\section{" ):
            tmp_line = line.strip()
            new_line = tmp_line[9:-1] + ".\n"
            output_text += process(new_line)
            continue


        if line.startswith( "\\begin" ):
            tmp_line = line.strip()
            if tmp_line.startswith( "\\begin{document}" ):
                continue
            else:
                in_figure = True
                continue

        tex_commands = [
            "maketitle",
            "end{document}",
            "usepackage",
            "documentclass",
            "newcommand",
            ]

        tex_command_line = False
        for tex_command in tex_commands:
            if line.startswith( "\\" + tex_command ):
                tex_command_line = True
        if tex_command_line:
            continue

        if in_figure:
            tmp_line = line.strip()
            if tmp_line.startswith( "\\alttext" ):
                figure_text = figure_text + process(tmp_line[9:-1].strip()) + "\n"
                continue
            if tmp_line.startswith( "\\caption{" ):
                figure_text = figure_text + process(tmp_line[9:-1].strip()) + "\n"
                continue

            if tmp_line.startswith( "\\end{figure}" ):
                output_text += process(figure_text) + "\n \n"
                in_figure = False
                continue
        else:
            if line.startswith( "%" ):
                continue
            else:
                output_text += process(line)
                continue
            

     
    if (debug >= 1): print output_text
    file.close()
       
    return output_text


def create_special_charicters():
    special_charicter_dict = {}
    
    special_charicters = [
    'alpha',
    ]

    for charicter in special_charicters:
        special_charicter_dict["\\" + charicter] = charicter

    return special_charicter_dict


def get_inputs(debug=0):

    # Gets the inputs from command line

    inputs = {}

    if (debug>=1): 
        inputs['tex_input_name']    = 'report.tex'
        inputs['text_output_name']  = 'report.txt'
        inputs['mp3_output_name']   = 'report.mp3'

    return inputs;



if __name__ == "__main__":
    main()    

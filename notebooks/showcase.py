from tf.app import use
import re
from IPython.display import display, HTML
import ipywidgets as widgets
import difflib

MT=use('etcbc/bhsa', hoist=globals())
Fmt, Lmt, Tmt = MT.api.F, MT.api.L, MT.api.T

MT.load('g_cons_utf8')

SP=use('dt-ucph/sp', hoist=globals())
Fsp, Lsp, Tsp = SP.api.F, SP.api.L, SP.api.T

class showcase:
    
    def __init__(self):
        
        print('Loading...')
        books = ['Genesis','Exodus','Leviticus','Numbers','Deuteronomy']
        
        def reconstruct_pentateuchal_verses(F, L, T, text_feature):
            """For each verse of the Pentateuch in a given dataset, the text of each verse is reconstructed.
            Output:
            verse_texts: dict   Keys are verse label (tuple with book, chapter verse), values are reconstructed text (str).
            """
            verse_texts = {}

            for verse_node in F.otype.s('verse'):
                bo, ch, ve = T.sectionFromNode(verse_node)
                if bo in books:
                    verse_text = ''
                    word_nodes = L.d(verse_node, 'word')
                    for word_node in word_nodes:
                        word_text = eval(f'F.{text_feature}.v(word_node)')
                        trailer = F.trailer.v(word_node)
                        if not word_text:
                            continue
                        elif not trailer:
                            verse_text += word_text
                        else:
                            verse_text += word_text + ' '
                    verse_text = re.sub('שׁ','שׁ',verse_text)
                    verse_text = re.sub('שׂ','שׂ',verse_text)
                    verse_texts[(bo, ch, ve)] = verse_text.strip()
            return verse_texts
    
        self.sp_verses = reconstruct_pentateuchal_verses(Fsp, Lsp, Tsp, 'g_cons_utf8')
        self.mt_verses = reconstruct_pentateuchal_verses(Fmt, Lmt, Tmt, 'g_cons_utf8')
        
        print('\nLoading completed')
        
    def showComparison(self, a, b):
        output = []
        matcher = difflib.SequenceMatcher(None, a, b)
        styling = 'font-size:34px;font-family:SBL Hebrew;line-height:150%;align:right;'
        for opcode, a0, a1, b0, b1 in matcher.get_opcodes():
            if opcode == "equal":
                output.append(f'<span style="{styling}">{a[a0:a1]}</span>')
            elif opcode == "insert":
                output.append(f'<span style="{styling}background-color:#1A85FF;">{b[b0:b1]}</span>') #blue
            elif opcode == "delete":
                output.append(f'<span style="{styling}background-color:#D41159;">{a[a0:a1]}</span>') #red
            elif opcode == "replace":
                output.append(f'<span style="{styling}background-color:#1A85FF;">{b[b0:b1]}</span>') #blue
                output.append(f'<span style="{styling}background-color:#D41159;">{a[a0:a1]}</span>') #red
        return "".join(output)

    def explore(self):
        
        FEATURES = ['g_cons','g_cons_utf8','g_nme','g_nme_utf8',
                    'g_pfm','g_pfm_utf8','g_prs','g_prs_utf8','lex_utf8','nu','ps','vt']
        
        a = widgets.SelectMultiple(
            options=FEATURES,
            rows=10,
            description='Features',
            disabled=False
        )

        b= widgets.Combobox(
            value='Genesis',
            options=['Genesis', 'Exodus', 'Leviticus', 'Numbers','Deuteronomy'],
            description='Book',
            ensure_option=True,
            disabled=False
        )

        c = widgets.IntText(
            value=1,
            description='Chapter',
            disabled=False
        )

        d = widgets.IntText(
            value=1,
            description='Verse',
            disabled=False
        )
        
        e = widgets.Checkbox(
            value=False,
            description='Compare with MT',
            disabled=False
        )

        def f(feature, book, chapter, verse, compare):
            try:
                SP.displaySetup(extraFeatures=feature, standardFeatures=True)
                SP.pretty(Tsp.nodeFromSection((book,chapter,verse)))
                if compare:
                    display(HTML('<p style="font-size:14px;color:#D41159;">Red colour: Absent in MT</p>'))
                    display(HTML('<p style="font-size:14px;color:#1A85FF;">Blue colour: Absent in SP</p>'))
                    display(HTML(self.showComparison(self.sp_verses[(book,chapter,verse)],self.mt_verses[(book,chapter,verse)])))
            except:
                print('\nWrong chapter or verse')

        out = widgets.interactive_output(f, {'feature': a, 'book': b, 'chapter': c, 'verse': d, 'compare': e})

        display(widgets.VBox([widgets.HBox([a,widgets.VBox([b, c, d, e])]), out]))
        
    def search(self):
        
        a = widgets.Text(
            value='על',
            description='Search',
            disabled=False
        )
        
        b = widgets.Checkbox(
            value=False,
            description='Only complete matches',
            disabled=False
        )
        
        def getDelete():
            out = {}
            n=0
            for v in self.sp_verses:
                matcher = difflib.SequenceMatcher(None, self.sp_verses[v], self.mt_verses[v])
                for opcode, a0, a1, b0, b1 in matcher.get_opcodes():
                    if opcode in {'delete','replace'}:
                        out[n] = (v, self.sp_verses[v][a0:a1])
                        n+=1      
            return out
        
        try:
            self.delete
        except:
            self.delete = getDelete()
            
        # Function to update the display
        def update_results():
            # Calculate the range of results to display
            start = self.counter
            end = min(self.counter + self.results_per_page, len(self.results))
            if start < len(self.results):
                text = ''
                for r in self.results[start:end]:
                    text += f'<p>{"""{} {}:{}""".format(*r)}</p>{self.showComparison(self.sp_verses[r],self.mt_verses[r])}'
                output_html.value = text  # Join results into a string with newlines
            
            elif not start and not end:
                output_html.value = ''
                
        # Function to show next 10 results
        def show_next_results(change=None):
            if self.counter + self.results_per_page < len(self.results):
                self.counter += self.results_per_page
                update_results()

        # Function to show previous 10 results
        def show_previous_results(change=None):
            if self.counter - self.results_per_page >= 0:
                self.counter -= self.results_per_page
                update_results()
        
        def f(input_text, complete_matches):

            results = []
            
            for v, text in self.delete.values():
                if complete_matches and input_text == text.strip():
                    results.append(v)
                elif not complete_matches and input_text in text:
                    results.append(v)
            
            self.results = list(sorted(set(results), key=results.index))
            display(HTML(f'{len(self.results)} result(s)'))

            # Initialize the counter to keep track of the current index
            self.counter = 0
            self.results_per_page = 10  # Number of results to show at a time

            update_results()
            # Create widgets            
            display(widgets.HBox([previous_button, next_button]))
            
        output_html = widgets.HTML(continuous_update=True)
        next_button = widgets.Button(description="Show Next 10 Results")
        previous_button = widgets.Button(description="Show Previous 10 results")

        # Attach the button click event to the function
        next_button.on_click(show_next_results)
        previous_button.on_click(show_previous_results)
        out = widgets.interactive_output(f, {'input_text': a, 'complete_matches': b})

        # Display the initial output
        display(widgets.HBox([a, b]), out)

        # Display the widgets
        display(output_html)
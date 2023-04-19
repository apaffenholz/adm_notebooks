
import ipywidgets as widgets
from IPython.display import HTML, display, clear_output
from traitlets import CInt

colors = ['#f99','#cde','#cc0','#fc2']

def set_delay(new_delay=300):
    global delay 
    delay = new_delay

def display_algo(frames):
    global delay
    count = len(frames)
    class Counter(widgets.DOMWidget):
        value = CInt(0, sync=True)

    def incr(name):
        counter.value += 1 if counter.value < count else 0

    def decr(name):
        counter.value -= 1 if counter.value > 0 else 0

    out = widgets.Output()
    def on_value_change(change):
        with out: 
            clear_output(wait=True)
            display(HTML(frames[change['new']]))

    counter = Counter()
    
    layout = widgets.Layout(width='40px')
    button_incr = widgets.Button(description='>',layout=layout)
    button_decr = widgets.Button(description='<',layout=layout)
    button_incr.on_click(incr)
    button_decr.on_click(decr)

    play = widgets.Play(
        value=0,
        min=0,
        max=len(frames)-1,
        step=1,
        interval=delay,
        description="Press play",
        disabled=False
    )
    slider = widgets.IntSlider(
        min=0,
        max=len(frames)-1,
        readout=False
    )

    slider.observe(on_value_change, 'value')
    on_value_change({'new':0})

    widgets.jslink((play, 'value'), (slider, 'value'))
    widgets.jslink((slider, 'value'), (counter, 'value'))
    
    box_play   = widgets.HBox([play, button_decr,button_incr])
    box_slider = widgets.HBox([slider])
    return widgets.VBox([box_play,box_slider,out])

def wrap_table(x):
    return '<style>td.largelist { font-size:200%; }</style><table>'+x+'</table>'

def wrap_table_ms(x):
    content = ""
    content += '<style>td.largelist { font-size:150%; }'
    content += 'td div{width:60px;height:30px;overflow:hidden;word-wrap:break-word;}'
    content += '</style><table>'
    content += x
    content +='</table>'
    return content

def generate_table_row(data,hi,hc):
    clear_output(wait=True)
    content = '<tr>'
    for i in range(len(data)):
        content += '<td  class="largelist" '
        if ( hi.count(i) ):
            content += ' style="background-color:' + colors[hc[hi.index(i)]] +'"'
        content += '>' + str(data[i]) + '</td>'
    content += '</tr>'
    return content

def _bubble_sort_display(x):
    frames = []
    final_frames = ''
    frames.append(
        wrap_table(final_frames+generate_table_row(x,[],[]))
    )
    length = len(x)-1
    finished_indices = []
    finished_colors = []
    for i in range(length,0,-1):
        for j in range(i):
            frames.append(
                wrap_table(
                    final_frames+
                    generate_table_row(x, [j,j+1]+finished_indices, [1,1]+finished_colors)
                )
            )
            if x[j] > x[j+1]:
                x[j], x[j+1] = x[j+1], x[j]
                frames.append(
                    wrap_table(                    
                        final_frames+
                        generate_table_row(x,[j,j+1]+finished_indices,[0,0]+finished_colors)
                    )
                )
            frames.append(
                wrap_table(               
                    final_frames
                    +generate_table_row(x,[]+finished_indices,[]+finished_colors)
                )
            )
        finished_indices.insert(0,i)
        finished_colors.insert(0,2)
        frames.append(
            wrap_table(            
                final_frames+
                generate_table_row(x,[]+finished_indices,[]+finished_colors)
            )
        )
        final_frames += generate_table_row(x,[]+finished_indices,[]+finished_colors,False)

    finished_indices.insert(0,0)
    finished_colors.insert(0,2)
    frames.append(
        wrap_table(        
            final_frames+
            generate_table_row(x,[]+finished_indices,[]+finished_colors)
        )
    )
    return frames

def _insertion_sort_display(x):
    frames = []
    final_frames = ''
    frames.append(wrap_table(final_frames+generate_table_row(x,[],[])))
    length = len(x)
    finished_indices = []
    finished_indices.insert(0,0)
    finished_colors = []
    finished_colors.insert(0,2)
    frames.append(
        wrap_table(
            final_frames+
            generate_table_row(x,finished_indices,finished_colors)
        )
    )
    for i in range(1,length):
        finished_indices.append(i)
        finished_colors.insert(0,2)
        b = x[i]
        k = i
        while( k >= 1 and x[k-1] > b):
            frames.append(
                wrap_table(
                    final_frames+
                    generate_table_row(x,[k]+finished_indices,[3]+finished_colors)
                )
            )
            x[k-1],x[k] = x[k],x[k-1]
            frames.append(
                wrap_table(
                    final_frames+
                    generate_table_row(x,[k-1]+finished_indices,[3]+finished_colors)
                )
            )
            k = k-1
        frames.append(
            wrap_table(
                final_frames+
                generate_table_row(x,[]+finished_indices,[]+finished_colors)
            )
        )
        final_frames += generate_table_row(x,[]+finished_indices,[]+finished_colors)
    return frames

def _selection_sort_display(x):
    frames = []
    final_frames = ''
    frames.append(wrap_table(final_frames+generate_table_row(x,[],[])))
    length = len(x)-1
    finished_indices = []
    finished_colors = []
    k = -1
    for i in range(length,0,-1):
        k = i
        for j in range(i):
            frames.append(
                wrap_table(
                    final_frames+
                    generate_table_row(x,[j,i]+finished_indices,[1,1]+finished_colors)
                )
            )
            if x[j] > x[k]:
                k = j
                frames.append(
                    wrap_table(
                        final_frames+generate_table_row(x,[i,j]+finished_indices,[0,0]+finished_colors)
                    )
                )
        frames.append(
            wrap_table(
                final_frames+generate_table_row(x,[i,k]+finished_indices,[3,3]+finished_colors)
            )
        )
        x[k], x[i] = x[i], x[k]
        finished_indices.insert(0,i)
        finished_colors.insert(0,2)
        frames.append(
            wrap_table(
                final_frames+
                generate_table_row(x,[]+finished_indices,[]+finished_colors)
            )
        )
        final_frames += generate_table_row(x,[]+finished_indices,[]+finished_colors)

    finished_indices.insert(0,0)
    finished_colors.insert(0,2)
    frames.append(
        wrap_table(
            final_frames+
            generate_table_row(x,[]+finished_indices,[]+finished_colors)
        )
    )
    return frames

def MergeSort_impl(data,l,u,init_rows):
    frames = []
    frames.append(wrap_table_ms(init_rows+mergesort_display(data,[l,u],[],[],[],[])))
    if ( u-l <= 0 ):
        return frames,init_rows
    m = l+int((u-l)/2)
    frames.append(wrap_table_ms(init_rows+mergesort_display(data,[l,m],[m+1,u],[],[],[])))
    f,i = MergeSort_impl(data,l,m,init_rows)
    frames += f
    init_rows = i
    f,i = MergeSort_impl(data,m+1,u,init_rows)
    frames += f
    init_rows = i
    i = l
    j = m+1
    temp = []
    data_temp = data.copy()
    for k in range(l,u+1):
        temp.append(data[k])
    k = l
    frames.append(wrap_table_ms(init_rows
                             +mergesort_display(data_temp,[l,m],[m+1,u],[],[],[])
                             +mergesort_display(data,[l,u],[],[],[],[k,u])))
    while ( i<=m and j<=u ):
        frames.append(wrap_table_ms(init_rows
                                 +mergesort_display(data_temp,[l,m],[m+1,u],[i,j],[3,3],[])
                                 +mergesort_display(data,[l,u],[],[],[],[k,u])))
        if ( temp[i-l] <= temp[j-l] ):
            data[k] = temp[i-l]
            frames.append(wrap_table_ms(init_rows
                                     +mergesort_display(data_temp,[l,m],[m+1,u],[i],[2],[])
                                     +mergesort_display(data,[l,u],[],[],[],[k,u])))
            i += 1
        else:
            data[k] = temp[j-l]
            frames.append(wrap_table_ms(init_rows
                                     +mergesort_display(data_temp,[l,m],[m+1,u],[j],[2],[])
                                     +mergesort_display(data,[l,u],[],[],[],[k,u])))
            j += 1
        k += 1
        frames.append(wrap_table_ms(init_rows
                                 +mergesort_display(data_temp,[l,m],[m+1,u],[],[],[])
                                 +mergesort_display(data,[l,u],[],[],[],[k,u])))        
    while ( i <= m ):
        data[k] = temp[i-l]
        frames.append(wrap_table_ms(init_rows
                                 +mergesort_display(data_temp,[l,m],[m+1,u],[i],[2],[])
                                 +mergesort_display(data,[l,u],[],[],[],[k,u])))
        i += 1
        k += 1
        frames.append(wrap_table_ms(init_rows
                                 +mergesort_display(data_temp,[l,m],[m+1,u],[],[],[])
                                 +mergesort_display(data,[l,u],[],[],[],[k,u])))
    while ( j <= u ):
        data[k] = temp[j-l]
        frames.append(wrap_table_ms(init_rows
                                 +mergesort_display(data_temp,[l,m],[m+1,u],[j],[2],[])
                                 +mergesort_display(data,[l,u],[],[],[],[k,u])))
        j += 1
        k += 1
        frames.append(wrap_table_ms(init_rows
                                 +mergesort_display(data_temp,[l,m],[m+1,u],[],[],[])
                                 +mergesort_display(data,[l,u],[],[],[],[k,u])))
    init_rows += mergesort_display(data_temp,[l,m],[m+1,u],[],[],[])+mergesort_display(data,[l,u],[],[],[],[])
    frames.append(wrap_table_ms(init_rows))
    return frames,init_rows

def mergesort_display(data,active,active_r,hi,hc,suppress):
    colors = ['#f99','#add','#cc0','#fc2','#ddd','#9cc']
    clear_output(wait=True)
    content = ""
    content += '<tr>'
    for i in range(len(data)):
        content += '<td  class="largelist" '
        content += ' style="background-color:'
        if ( i>= active[0] and i <=active[1] or (len(active_r)>1 and (i>= active_r[0] and i <=active_r[1])) ):
            if ( hi.count(i) ):
                content += colors[hc[hi.index(i)]]
            else:
                if ( len(active_r)>1 and (i>= active_r[0] and i <=active_r[1]) ):
                    content += colors[5]
                else:
                    content += colors[1]                
        else:
            content += colors[4]
        content += '"'
        content += '>'
        if ( len(suppress) <= 0 or i< suppress[0] or i > suppress[1] ):
            content += str(data[i])
        content += '</td>'
    content += '</tr>'
    return content

def BubbleSort(data):
    frames = _bubble_sort_display(data)
    return display_algo(frames)

def SelectionSort(data):
    frames = _selection_sort_display(data)
    return display_algo(frames)

def InsertionSort(data):
    frames = _insertion_sort_display(data)
    return display_algo(frames)

def MergeSort(A):
    frames,i=MergeSort_impl(A,0,len(A)-1,"")
    return display_algo(frames)
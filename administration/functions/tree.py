def get_substep_tree_as_nested_list(substeps):
    temp = []
    
    if not substeps:
        return ''
    
    for substep in substeps:
        temp.append(substep['title'])
        substeps = get_substep_tree_as_nested_list(substep['substeps'])
        if substeps:
            temp.append(substeps)

    return temp

def get_decision_tree_as_nested_list(decisionsteps):
    temp = []
    
    if not decisionsteps:
        return ''
    
    for substep in decisionsteps:
        temp.append(substep['title'])
        decisionsteps = get_decision_tree_as_nested_list(substep['decisionsteps'])
        if decisionsteps:
            temp.append(decisionsteps)

    return temp

def render_tree(step, parent=False):
    rendered = []
    rendered.append('<li>')  # New list item
    if not parent:
        rendered.append(step['title'])  # Add the step title
    
    if step['decisionsteps']:  # is a DecisionStep
        rendered.append('<ul class="decisiontree">')  # Start a new list
        for decisionstep in step['decisionsteps']:
            rendered += (render_tree(decisionstep))  # Recursion
        rendered.append('</ul>')  # End the list
        
    if step['substeps']:  # is a SuperStep
        rendered.append('<ul>')  # Start a new list
        for substep in step['substeps']:
            rendered += (render_tree(substep))  # Recursion
        rendered.append('</ul>')  # End the list
    
    rendered.append('</li>')  # End list item

    return rendered
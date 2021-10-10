def get_tree_as_nested_list(substeps):
    temp = []
    
    if not substeps:
        return ''
    
    for substep in substeps:
        temp.append(substep['title'])
        substeps = get_tree_as_nested_list(substep['substeps'])
        if substeps:
            temp.append(substeps)

    return temp
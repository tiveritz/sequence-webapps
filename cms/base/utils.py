def apply_positions(context, parent_position=None):
    for pos, link in enumerate(context['linked'], 1):
        if parent_position is None:
            position = str(pos)
        else:
            position = '{}.{}'.format(parent_position, pos)
        
        link['pos'] = position
        apply_positions(link, position)
        pos += 1

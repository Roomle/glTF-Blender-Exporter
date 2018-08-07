import bpy
import logging

def get_base_color_input(color_socket):
    if not isinstance(color_socket, bpy.types.NodeSocketColor):
        logging.error('Not a color socket')
        return None

    if not color_socket.is_linked:
        return color_socket.default_value
    else:
        from_node = color_socket.links[0].from_node
        return get_base_color(from_node)

def get_base_color_rgb(rgb_node):
    return rgb_node.outputs['Color'].default_value

def get_base_color_mix(mix_node):

    color1 = get_base_color_input(mix_node.inputs['Color1'])
    color2 = get_base_color_input(mix_node.inputs['Color2'])

    if color2:
        if color1:
            if mix_node.blend_type == 'MULTIPLY':
                return [ x[0]*x[1] for x in zip(color1,color2)]
        return color2
    if color1:
        return color1

    return None

def get_base_color(node):
    print( 'get_base_color {}'.format(type(node)))
    if isinstance(node, bpy.types.ShaderNodeRGB):
        return get_base_color_rgb(node)
    elif isinstance(node, bpy.types.ShaderNodeMixRGB):
        return get_base_color_mix(node)
    elif isinstance(node, bpy.types.ShaderNodeBsdfPrincipled):
        return get_base_color_principled(node)
    return None

def get_base_color_principled(principled_node):
    return get_base_color_input(principled_node.inputs['Base Color'] )

def get_normal_strength(principled_node):
    socket = principled_node.inputs['Normal']
    if socket.is_linked:
        norm_node = socket.links[0].from_node
        socket = norm_node.inputs['Strength']
        if socket.is_linked:
            node = socket.links[0].from_node
            if isinstance(node, bpy.types.ShaderNodeValue):
                return node.outputs['Value'].default_value
        else:
            return socket.default_value
    return None
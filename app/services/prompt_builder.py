def build_prompt(text_input):

    style = text_input.get("style")
    color_tone = text_input.get("color_tone")
    room_type = text_input.get("room_type")
    to_remove = text_input.get("to_remove", [])
    to_add = text_input.get("to_add", [])

    remove_text = ""
    add_text = ""

    if to_remove:
        remove_text = "Remove the following items from the room: " + \
            ", ".join(to_remove) + "."

    if to_add:
        add_text = "Add the following items to the room: " + \
            ", ".join(to_add) + "."

    prompt = f"""
      Redesign the interior of the provided {room_type} photo.

      Keep the original room structure, layout, walls, windows, and camera perspective the same.

      Apply a {style} interior design style with a {color_tone} color palette.

      {remove_text}

      {add_text}

      The result should be photorealistic and look like a professionally designed interior.
      Do not change the room architecture or viewpoint.
      """

    return prompt.strip()

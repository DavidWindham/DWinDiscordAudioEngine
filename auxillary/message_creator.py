from discord import Embed


def get_embedded_message_from_queue(queue):
    embedded_message = Embed(title="Queue", color=0xeb4034)

    if len(queue) == 0:
        embedded_message.add_field(name="Empty", value="Add some tunes", inline=False)
        return embedded_message
    for idx, item in enumerate(queue):
        if idx == 0:
            get_single_item_field(embedded_message, item, name_prefix="Now Playing: ")
            embedded_message.set_image(url=item.thumbnail_link)
        else:
            get_single_item_field(embedded_message, item, name_prefix=str(idx) + ". ")
    return embedded_message


def get_single_item_field(embed, item, name_prefix):
    embed.insert_field_at(
        index=0,
        name=name_prefix + item.title,
        value=str(item.duration_string),
        inline=False
    )

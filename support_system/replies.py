"""Recursive reply/follow-up display for the support request system."""


def display_replies(replies, index=0):
    """
    Recursively display replies in order.
    Time complexity: O(n) where n = number of replies
    Space complexity: O(n) due to recursion stack
    
    Args:
        replies: List of reply strings
        index: Current index (starts at 0)
    
    Returns:
        List of formatted reply strings
    """
    # Base case: no more replies to display
    if index >= len(replies):
        return []
    
    # Display current reply and recurse for the rest
    current_reply = f"Reply {index + 1}: {replies[index]}"
    return [current_reply] + display_replies(replies, index + 1)


def display_replies_indented(replies, index=0, indent_level=0):
    """
    Recursively display replies with indentation for threaded view.
    Useful for showing follow-up replies to replies.
    
    Time complexity: O(n)
    Space complexity: O(n) due to recursion stack
    """
    if index >= len(replies):
        return []
    
    indent = "  " * indent_level
    current_reply = f"{indent}Reply {index + 1}: {replies[index]}"
    # Increment indent_level for next recursive call to show threaded depth
    return [current_reply] + display_replies_indented(replies, index + 1, indent_level + 1)
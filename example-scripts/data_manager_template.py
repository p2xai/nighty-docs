@nightyScript(
    name="Simple Notes",
    author="AutoGPT",
    description="Store and manage short notes.",
    usage="<p>addnote <text> | <p>notes | <p>delnote <index>"
)
def script_function():
    """
    DATA MANAGER TEMPLATE
    ---------------------

    Saves small pieces of text to a JSON file.

    COMMANDS:
    <p>addnote <text> - Add a note
    <p>notes - List all notes
    <p>delnote <index> - Remove a note by number

    NOTES:
    - Uses a simple JSON file named `notes.json`
    - Demonstrates the data management pattern (Section 6.5)
    """
    import json
    from pathlib import Path

    DATA_FILE = Path("notes.json")

    def load_notes():
        if DATA_FILE.exists():
            with DATA_FILE.open("r") as f:
                return json.load(f)
        return []

    def save_notes(notes):
        with DATA_FILE.open("w") as f:
            json.dump(notes, f)

    @bot.command(name="addnote", description="Add a note.")
    async def add_note_cmd(ctx, *, text: str):
        await ctx.message.delete()
        notes = load_notes()
        notes.append(text)
        save_notes(notes)
        await ctx.send("Note added.", silent=True)

    @bot.command(name="notes", description="List notes.")
    async def list_notes_cmd(ctx):
        await ctx.message.delete()
        notes = load_notes()
        if notes:
            msg = "\n".join(f"{i+1}. {n}" for i, n in enumerate(notes))
            await ctx.send(msg, silent=True)
        else:
            await ctx.send("No notes saved.", silent=True)

    @bot.command(name="delnote", description="Delete a note by number.")
    async def del_note_cmd(ctx, index: str):
        await ctx.message.delete()
        try:
            i = int(index) - 1
        except ValueError:
            await ctx.send("Index must be a number.", silent=True)
            return
        notes = load_notes()
        if 0 <= i < len(notes):
            removed = notes.pop(i)
            save_notes(notes)
            await ctx.send(f"Removed note: {removed}", silent=True)
        else:
            await ctx.send("Invalid index.", silent=True)

script_function()

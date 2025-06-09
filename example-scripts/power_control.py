@nightyScript(
    name="Power Control",
    author="OpenAI",
    description="Commands to reboot, shut down or lock the host machine.",
    usage="<p>reboot OR <p>shutdown OR <p>lock"
)
def power_control():
    """
    POWER CONTROL
    -------------
    Provides three commands to reboot, shut down or lock the system.

    COMMANDS:
    <p>reboot   - Immediately restart the machine.
    <p>shutdown - Immediately power off the machine.
    <p>lock     - Lock the current session.

    NOTES:
    - Requires appropriate OS permissions to perform these actions.
    - Works on Windows and Linux.
    """

    import os
    import platform
    import subprocess

    @bot.command(name="reboot", description="Restart the machine")
    async def reboot_command(ctx):
        await ctx.message.delete()
        try:
            if platform.system() == "Windows":
                os.system("shutdown /r /t 0")
            else:
                subprocess.run(["shutdown", "-r", "now"])
        except Exception as e:
            await ctx.send(f"Failed to reboot: {e}")

    @bot.command(name="shutdown", description="Shut down the machine")
    async def shutdown_command(ctx):
        await ctx.message.delete()
        try:
            if platform.system() == "Windows":
                os.system("shutdown /s /t 0")
            else:
                subprocess.run(["shutdown", "-h", "now"])
        except Exception as e:
            await ctx.send(f"Failed to shut down: {e}")

    @bot.command(name="lock", description="Lock the machine")
    async def lock_command(ctx):
        await ctx.message.delete()
        try:
            if platform.system() == "Windows":
                os.system("rundll32.exe user32.dll,LockWorkStation")
            else:
                # Use loginctl or xdg-screensaver if available
                if subprocess.run(["which", "loginctl"], capture_output=True).returncode == 0:
                    subprocess.run(["loginctl", "lock-session"])
                else:
                    subprocess.run(["xdg-screensaver", "lock"])
        except Exception as e:
            await ctx.send(f"Failed to lock: {e}")

power_control()

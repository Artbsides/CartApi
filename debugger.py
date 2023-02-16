import debugpy
import multiprocessing


def debugger(debug_port):
    if multiprocessing.current_process().pid > 1:
        debugpy.listen(("0.0.0.0", int(debug_port)))

        print("")
        print("⏳ VS Code debugger can now be attached, port={}".format(debug_port), flush=True)

        debugpy.wait_for_client()

        print("🎉 VS Code debugger attached", flush=True)
        print("")

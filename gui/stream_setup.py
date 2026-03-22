# Anpassung der funktionierenden 'GoProStream.py' von KonradIT an GPJ-Projekt

### IMPORTS ###
import time
import requests         # -> für http-requests
import subprocess       # -> zum ausführen von ffmpeg
import threading        # ->
import socket           # -> für UDP Keep-Alive-message

class GoProClient:
    def __init__(self, ip="10.5.5.9"):
        self.ip = ip
        self.base_url = f"http://{ip}"
        self.keep_alive_running = False

    def start_stream(self):
        """Startet den Livestream auf der GoPro mit http-request"""
        url = f"{self.base_url}/gp/gpControl/execute"
        params = {
            "p1": "gpStream",
            #"a1": "proto_v2",   #test weil auch in vorlage enthalten
            "c1": "restart"}

        response = requests.get(url, params=params)

        if response.status_code == 200:
            print("Stream gestartet")
            return True #Test
        else:
            print("Fehler beim Starten")
            return False #Test

    def _keep_alive(self):
        """NICHT EINZELN AUFRUFEN
        Sendet regelmäßig UDP Keep-Alive Pakete"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = b"_GPHD_:0:0:2:0\n"

        while self.keep_alive_running:
            sock.sendto(message, (self.ip, 8554))
            time.sleep(2.5)

    def start_keep_alive(self):
        """startet periodische keep-Alive Anfragen bis 'stop_keep_alive() ausgeführt wird'"""
        self.keep_alive_running = True
        thread = threading.Thread(target=self._keep_alive, daemon=True)
        thread.start()

    def stop_keep_alive(self):
        self.keep_alive_running = False


    def show_stream(self):
        """Startet ffplay zur direkten Anzeige des Streams"""
        cmd = [
            "ffplay",
            "-fflags", "nobuffer",
            "-f:v", "mpegts",
            "udp://10.5.5.9:8554"]
        subprocess.run(cmd)

    def start_proxy_stream(self):
        """startet Thread für decoding mit ffmpeg und internes restreaming auf Port 5000"""
        cmd_old = [
            "ffmpeg",
            "-fflags", "nobuffer",
            "-f:v", "mpegts",
            "-probesize", "8192",
            "-i", "udp://10.5.5.9:8554",
            "-f", "mpegts",
            "-vcodec", "copy",
            "udp://127.0.0.1:5000"
        ]
        cmd = [
    "ffmpeg",
    "-fflags", "nobuffer",
    "-flags", "low_delay",
    "-fflags", "+genpts",
    "-i", "udp://10.5.5.9:8554",
    "-f", "mpegts",
    "-vcodec", "copy",
    "udp://127.0.0.1:5000"]
        self.ffmpeg_process = subprocess.Popen(cmd)
### folgendes ersetzt durch self.ffmpeg_process
#        thread = threading.Thread(
#            target=subprocess.Popen,
#            args=(cmd,),
#            daemon=True)
#        thread.start()    

    def stop_proxy_stream(self):
        if hasattr(self, "ffmpeg_process"):
            self.ffmpeg_process.terminate()
            self.ffmpeg_process.wait()

'''nicht nutzbar aktuell
    def start(self):
        """Startet alles"""
        self.start_stream()
        self.start_keep_alive()
        self.show_stream()

    def stop(self):
        """stoppt (alles?)"""
        self.stop_keep_alive()
'''

# Tests:
'''
mygp = GoProClient()
mygp.start()
'''
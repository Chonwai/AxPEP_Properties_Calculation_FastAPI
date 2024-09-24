from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import peptides

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.handle_calculate()

    def handle_calculate(self):
        query_components = parse_qs(urlparse(self.path).query)
        sequence = query_components.get("sequence", [None])[0]

        if sequence:
            try:
                result = self.calculate_properties(sequence)
                response = {
                    "status": "success",
                    "data": result
                }
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))
            except Exception as e:
                response = {
                    "status": "failed",
                    "error": {
                        "message": str(e)
                    }
                }
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            response = {
                "status": "failed",
                "error": {
                    "message": "No sequence provided"
                }
            }
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))

    def calculate_properties(self, sequence):
        analysis = ProteinAnalysis(sequence)
        properties = {
            "sequence": sequence,
            "length": len(sequence),
            "molecular_weight": analysis.molecular_weight(),
            "isoelectric_point": analysis.isoelectric_point(),
            "gravy": analysis.gravy(),
            "charge": analysis.charge_at_pH(7),
            "hydrophobic_moment": peptides.Peptide(sequence).hydrophobic_moment()
        }
        return properties

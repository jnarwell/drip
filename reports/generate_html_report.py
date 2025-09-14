import pandas as pd
import json

# Generate HTML report
html = """
<html>
<head><title>Acoustic Manufacturing System</title></head>
<body>
<h1>System Requirements Status</h1>
<table border="1">
<tr><th>Component</th><th>COTS Option</th><th>Cost</th><th>Lead Time</th></tr>
<tr><td>Transducers</td><td>APC International</td><td>$185/unit</td><td>4 weeks</td></tr>
<tr><td>FPGA</td><td>Intel Cyclone V</td><td>$485</td><td>2 weeks</td></tr>
<tr><td>Thermal Camera</td><td>Optris PI 1M</td><td>$12,000</td><td>6 weeks</td></tr>
</table>
</body>
</html>
"""
with open('reports/system_report.html', 'w') as f:
    f.write(html)
print("Report generated: reports/system_report.html")

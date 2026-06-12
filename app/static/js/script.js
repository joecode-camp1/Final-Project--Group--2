
    // Handles the smooth micro-interaction exit animation
    function dismissToast(toastId) {
        const toast = document.getElementById(toastId);
        if (toast) {
            toast.classList.add('opacity-0', 'scale-95', '-translate-y-2');
            setTimeout(() => {
                toast.remove();
            }, 300);
        }
    }
    
    // Auto-dismiss success flash messages after 6 seconds natively
    document.addEventListener("DOMContentLoaded", () => {
        // Find all toast alerts on the page using a generic attribute query
        const alerts = document.querySelectorAll('[id^="flash-toast-"]');
        
        alerts.forEach((toast) => {
            // Check if the toast element contains green success style identifiers
            if (toast.classList.contains('bg-emerald-950/40')) {
                setTimeout(() => {
                    dismissToast(toast.id);
                }, 6000);
            }
        });
    });

    // 1. EXCEL EXPORT ENGINE (SheetJS)
function exportToExcel() {
    const table = document.getElementById("audit-table");
    
    // Scrapes the HTML table structure and converts it to a clean spreadsheet data array
    const workbook = XLSX.utils.table_to_book(table, { sheet: "Attendance Logs" });
    
    // Generates the download trigger wrapper file block
    XLSX.writeFile(workbook, `Attendance_Report_${new Date().toISOString().slice(0,10)}.xlsx`);
}

// 2. PDF EXPORT ENGINE (jsPDF + AutoTable Extension)
function exportToPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF('l', 'mm', 'a4'); // 'l' format opens the document in landscape to avoid clipping rows!

    // Header Metadata Title Configurations
    doc.setFont("helvetica", "bold");
    doc.setFontSize(16);
    doc.text("INSTRUCTOR ATTENDANCE SYSTEM DIAGNOSTIC REPORT", 14, 15);
    
    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);
    doc.text(`Generated Timestamp: ${new Date().toLocaleString()}`, 14, 22);

    // Targets the DOM node structure element and builds the layout automatically
    doc.autoTable({
        html: '#audit-table',
        startY: 28,
        theme: 'grid',
        styles: { fontSize: 8, font: 'helvetica' },
        headStyles: { fillColor: [30, 41, 59], textColor: [255, 255, 255], fontStyle: 'bold' }, // slate-800 look
        alternateRowStyles: { fillColor: [248, 250, 252] },
        margin: { top: 30, right: 14, bottom: 15, left: 14 }
    });

    // Forces browser stream download array save sequence
    doc.save(`Attendance_Report_${new Date().toISOString().slice(0,10)}.pdf`);
}
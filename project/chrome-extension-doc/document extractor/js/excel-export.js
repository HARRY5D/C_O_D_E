function exportToExcel(numbers) {
    const ws = XLSX.utils.json_to_sheet(
        numbers.map(num => ({ value: num }))
    );
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Numbers");
    XLSX.writeFile(wb, "extracted_numbers.xlsx");
}

document.getElementById('processBtn').addEventListener('click', async () => {
    const file = document.getElementById('fileInput').files[0];
    if (!file) return;

    try {
        let numbers;
        if (file.type === 'application/pdf') {
            const pdfParser = new PdfParser();
            numbers = await pdfParser.extractNumbers(file);
        } else if (file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
            const wordParser = new WordParser();
            numbers = await wordParser.extractNumbers(file);
        }
        
        const numbersList = document.getElementById('numbersList');
        numbersList.innerHTML = numbers.join(', ');
        document.getElementById('exportBtn').disabled = false;
    } catch(error) {
        console.error('Error processing file:', error);
    }
});

document.getElementById('exportBtn').addEventListener('click', () => {
    const numbers = document.getElementById('numbersList')
        .innerHTML.split(', ')
        .map(num => parseFloat(num));
    exportToExcel(numbers);
});
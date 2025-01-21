class PdfParser {
    async extractNumbers(file) {
        const reader = new FileReader();
        
        return new Promise((resolve, reject) => {
            reader.onload = async function(event) {
                try {
                    const typedarray = new Uint8Array(event.target.result);
                    const pdf = await pdfjsLib.getDocument(typedarray).promise;
                    const numbers = [];
                    
                    for(let i = 1; i <= pdf.numPages; i++) {
                        const page = await pdf.getPage(i);
                        const content = await page.getTextContent();
                        const text = content.items.map(item => item.str).join(' ');
                        const matches = text.match(/\d+\.?\d*/g);
                        if(matches) {
                            numbers.push(...matches.map(num => parseFloat(num)));
                        }
                    }
                    
                    resolve(numbers);
                } catch(error) {
                    reject(error);
                }
            };
            reader.readAsArrayBuffer(file);
        });
    }
}
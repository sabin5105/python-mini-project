const textToPaste = `text to paste`;

// 특정 입력 필드에 강제로 텍스트 입력 (textarea를 찾아 선택)
const textArea = document.querySelector('textarea');
if (textArea) {
    textArea.value = textToPaste;
    textArea.dispatchEvent(new Event('input', { bubbles: true }));
    console.log('텍스트가 입력되었습니다.');
} else {
    console.error('텍스트 입력 필드를 찾을 수 없습니다.');
}

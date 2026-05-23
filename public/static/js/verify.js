
  // تبدیل اعداد فارسی/عربی به انگلیسی
  function convertNumbersInstant(input) {
    const cursorPosition = input.selectionStart;
    const persianToEnglish = {
      '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
      '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',
      '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
      '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
    };

    let convertedValue = '';
    for (let char of input.value) {
      convertedValue += persianToEnglish[char] || char;
    }

    input.value = convertedValue;
    input.setSelectionRange(cursorPosition, cursorPosition);
  }

  // مدیریت حرکت خودکار بین فیلدهای OTP
  document.addEventListener('DOMContentLoaded', function () {
    const inputs = document.querySelectorAll('.otp-input');

    inputs.forEach((input, index) => {
      input.addEventListener('input', function (e) {
        // تبدیل اعداد فارسی/عربی به انگلیسی
        convertNumbersInstant(input);

        // فیلتر کردن فقط اعداد
        input.value = input.value.replace(/[^0-9]/g, '');

        // اگر مقدار وارد شد و فیلد بعدی وجود داشت، فوکوس را منتقل کن
        if (input.value.length === 1 && index < inputs.length - 1) {
          inputs[index + 1].focus();
        }

        // به‌روزرسانی مقدار hidden input
        updateHiddenOTP();
      });

      input.addEventListener('keydown', function (e) {
        // اگر Backspace زد و فیلد خالی بود، به فیلد قبلی برگرد
        if (e.key === 'Backspace' && input.value === '' && index > 0) {
          inputs[index - 1].focus();
        }
      });

      input.addEventListener('paste', function (e) {
        e.preventDefault();
        const pastedData = e.clipboardData.getData('text').replace(/[^0-9]/g, '').split('');
        let currentIndex = index;

        pastedData.forEach(char => {
          if (currentIndex < inputs.length) {
            inputs[currentIndex].value = char;
            convertNumbersInstant(inputs[currentIndex]);
            currentIndex++;
          }
        });

        // فوکوس روی آخرین فیلد پر شده یا بعدی
        if (pastedData.length > 0) {
          const nextIndex = Math.min(index + pastedData.length, inputs.length - 1);
          inputs[nextIndex].focus();
          updateHiddenOTP();
        }
      });
    });

    // به‌روزرسانی مقدار فیلد مخفی (otp) با ترکیب تمام اعداد
    function updateHiddenOTP() {
      const otpValue = Array.from(inputs).map(inp => inp.value || '').join('');
      document.getElementById('otp').value = otpValue;
    }

    // فعال‌سازی فوکوس روی اولین فیلد خالی یا اولین فیلد
    const firstEmptyInput = [...inputs].find(input => !input.value);
    (firstEmptyInput || inputs[0]).focus();
  });

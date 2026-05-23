document.addEventListener('DOMContentLoaded', function() {
  // عناصر DOM
  const loginForm = document.getElementById('login-form');
  const otpForm = document.getElementById('otp-form');
  const otpInputs = document.querySelectorAll('.otp-input');
  const hiddenOtpInput = document.getElementById('otp');
  const resendOtpLink = document.querySelector('.resend-otp');
  const mobileInput = document.getElementById('mobile');
  const otpInvalidFeedback = document.querySelector('.otp-invalid-feedback');

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

  // اعتبارسنجی شماره موبایل
  function validateMobileNumber(input) {
    const mobileRegex = /^09[0-9]{9}$/;
    if (input.value.length === 0) {
      input.classList.remove('is-valid');
      input.classList.remove('is-invalid');
      return false;
    } else if (mobileRegex.test(input.value)) {
      input.classList.remove('is-invalid');
      input.classList.add('is-valid');
      return true;
    } else {
      input.classList.remove('is-valid');
      input.classList.add('is-invalid');
      return false;
    }
  }

  // به روز رسانی فیلد مخفی OTP
  function updateHiddenOtpField() {
    let otpValue = '';
    otpInputs.forEach(input => {
      otpValue += input.value;
    });
    hiddenOtpInput.value = otpValue;
  }

  // اعتبارسنجی فیلدهای OTP
  function validateOtpFields() {
    let allValid = true;
    otpInputs.forEach(input => {
      if (input.value === '') {
        input.classList.add('is-invalid');
        allValid = false;
      } else {
        input.classList.remove('is-invalid');
      }
    });
    return allValid;
  }

  // مدیریت فیلد موبایل
  mobileInput.addEventListener('input', function() {
    convertNumbersInstant(this);
    validateMobileNumber(this);
  });

  // ارسال فرم ورود
  loginForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    if (!validateMobileNumber(mobileInput)) {
      return;
    }
    
    const mobile = mobileInput.value;
    console.log('ارسال کد تایید به:', mobile);
    
    loginForm.classList.add('d-none');
    otpForm.classList.remove('d-none');
    otpInputs[0].focus();
  });

  // مدیریت فیلدهای OTP
  otpInputs.forEach((input, index) => {
    input.addEventListener('input', function(e) {
      // حذف کاراکترهای غیرعددی
      this.value = this.value.replace(/[^0-9]/g, '');
      
      // حذف وضعیت خطا
      this.classList.remove('is-invalid');
      otpInvalidFeedback.style.display = 'none';
      
      // حرکت به فیلد بعدی
      if (this.value.length === 1) {
        if (index < otpInputs.length - 1) {
          otpInputs[index + 1].focus();
        } else {
          this.blur();
        }
      }
      
      updateHiddenOtpField();
    });
    
    input.addEventListener('keydown', function(e) {
      // مدیریت کلید Backspace
      if (e.key === 'Backspace' && this.value === '' && index > 0) {
        otpInputs[index - 1].focus();
      }
    });
    
    input.addEventListener('blur', function() {
      // اعتبارسنجی هنگام از دست دادن فوکوس
      if (this.value === '' && otpForm.classList.contains('was-validated')) {
        this.classList.add('is-invalid');
      }
    });
  });

  // ارسال مجدد کد
  resendOtpLink.addEventListener('click', function(e) {
    e.preventDefault();
    console.log('ارسال مجدد کد تایید');
    
    otpInputs.forEach(input => {
      input.value = '';
      input.classList.remove('is-invalid');
    });
    otpInputs[0].focus();
    updateHiddenOtpField();
    otpInvalidFeedback.style.display = 'none';
  });

  // ارسال فرم OTP
  otpForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    if (!validateOtpFields()) {
      otpInvalidFeedback.style.display = 'block';
      
      return;
    }
    
    const otp = hiddenOtpInput.value;
    if (otp.length === 4) {
      console.log('کد تایید وارد شده:', otp);
      // ارسال فرم یا انجام عملیات بعدی
      this.submit();
    } else {
      otpInvalidFeedback.style.display = 'block';
      otpForm.classList.add('was-validated');
    }
  });
});
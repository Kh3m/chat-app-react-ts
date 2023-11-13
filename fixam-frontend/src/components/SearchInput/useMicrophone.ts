import { RefObject, useEffect, useState } from "react";

const useMicrophone = (
  micRef: RefObject<HTMLSpanElement>,
  searchRef: RefObject<HTMLInputElement>
) => {
  const [isListening, setIsListening] = useState(false);
  const [searchText, setSearchText] = useState("");
  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      // recognition.continuous = false;
      recognition.lang = "en-US";

      if (micRef && micRef.current)
        micRef.current.addEventListener("click", () => {
          recognition.start();
        });

      //  Events for Web Speech API
      recognition.onstart = () => {
        setIsListening(true);
      };

      recognition.onend = () => {
        setIsListening(false);
        searchRef.current?.focus();
        console.log(`END and isListening: ${isListening}`);
      };

      recognition.onresult = (event: SpeechRecognitionEvent) => {
        const result = event.results[0][0].transcript;
        if (searchRef && searchRef.current) {
          searchRef.current.value = result;
          setSearchText(searchRef.current.value);
        }
      };
    } else {
      console.log("YOUR BROWSER DOESN't SUPPORT SPEACH RECOGNITION");
    }
  }, [isListening]);

  return {
    isListening,
    searchText,
    setSearchText,
  };
};

export default useMicrophone;

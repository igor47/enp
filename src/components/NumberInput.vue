<template>
  <form>
      <div v-for="(item, index) in numbers" key="`row${index}`">
          <label :for="`number${index}`">Number {{index}}</label>
          <input
              type="text"
              width="3"
              :name="`number${index}`"
              :value="invalidValues[index] === undefined ? numbers[index] : invalidValues[index]"
              @change="updateNumberAt(index, $event)"
              :class="{ invalid: (invalidValues[index] !== undefined) }"
          />
          <button
              type="button"
              v-if="invalidValues[index] !== undefined"
              @click.prevent="() => { invalidValues[index] = undefined; }"
              >Clear</button>
      </div>

      <div>
          <label :for="numbers.length">Number {{numbers.length}}</label>
          <input
              type="text"
              width="3"
              v-model="newNum"
              @change="updateNumberAt(numbers.length, $event)"
              :class="{ invalid: (invalidValues[numbers.length] !== undefined) }" />
      </div>

      <button
          type="button"
          @click.prevent="printNumbers"
          >Print</button>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue'

const numbers = ref([1, 2, 3])
const invalidValues = ref([])
const newNum = ref("")

const updateNumberAt = (idx, event) => {
    const oldv = numbers.value[idx]
    const newv = event.target.value;
    const isNew = idx === numbers.value.length;

    if (isNaN(newv * 1)) {
        invalidValues.value[idx] = newv;
    } else {
        invalidValues.value[idx] = undefined;

        if (newv === "") {
            delete numbers.value[idx]
            numbers.value = numbers.value.filter((val) => (val === 0 || !!val))
        } else {
            numbers.value[idx] = newv * 1

            if (isNew) {
                newNum.value = "";
            }
        }
    }
}

const printNumbers = () => {
    const data = JSON.stringify({
        numbers: numbers.value,
    });

    fetch(
        "/api/print_numbers",
        {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: data,
        },
    ).then(response => {
        response.blob().then(blob => {
            //Create a link element, hide it, direct it towards the blob, and then 'click' it programatically
            let a = document.createElement("a");
            a.style = "display: none";
            document.body.appendChild(a);

            //Create a DOMString representing the blob and point the link element towards it
            let url = window.URL.createObjectURL(blob);
            a.href = url;
            a.setAttribute('download', 'numbers.pdf');
            a.setAttribute('target', '_blank');

            //programatically click the link to trigger the download
            a.click();

            //release the reference to the file by revoking the Object URL
            window.URL.revokeObjectURL(url);
        });
    });
}
</script>

<style>
input {
    border: 1px solid black;
    margin: 1em 2px;
}

input.invalid {
    border: 1px dashed red;
}
</style>

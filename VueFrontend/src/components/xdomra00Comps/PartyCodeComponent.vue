

<template>
    <div class="flex three center">
        <div class="full">
            <h3 style="padding: 0;">Party code</h3>
            <h1 style="padding: 0;">{{ code }}</h1>
        </div>
        <button @click="this.$emit('readyPressed')" class="two-third" :class="!ready ? 'greenBack':  'redBack'">
            <h2 class="zeroPad blackColor">
                {{!ready ? "Ready" : "Cancel"}}
            </h2>
        </button>
    </div>
    
</template>


<script>

export default {
        props: ['code', 'ready'],
        data()
        {
            return {
            }
        },
    
        methods: {
        }
    }


</script>


<style>


</style>
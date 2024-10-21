

<template>

    <div class="flex one textCenter">
        <h3 class="full">Start Writing!</h3>
        <h3 class="full">{{ minutesLeft }}:{{ secondsLeft.toString().padStart(2, '0') }}</h3>
        <textarea  class=" full" style="resize: none;" rows=8 placeholder="New flavor of ice cream"></textarea>
    </div>

</template>


<script>

    export default {

        props: ['timeToWait'],

        mounted()
        {
            
        },

        data() 
        {
            return {
                timeLeft: 61
            }
        },

        computed: {

            minutesLeft() 
            {
                let tl = this.timeLeft;
                return Math.floor(tl / 60);
            },

            secondsLeft()
            { 
                let tl = this.timeLeft;
                return tl % 60; 
            }

        } 
    }

</script>


<style scoped>

</style>
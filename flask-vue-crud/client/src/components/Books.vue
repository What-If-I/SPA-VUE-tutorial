<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Books</h1>
        <hr>
        <br><br>
        <alert ref="alert"></alert>
        <button type="button" class="btn btn-success btn-sm"
                v-b-modal.book-modal>Add Book
        </button>
        <br><br>
        <table class="table table-hover">
          <thead>
          <tr>
            <th scope="col">Title</th>
            <th scope="col">Author</th>
            <th scope="col">Read?</th>
            <th></th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(book, index) in books" :key="index">
            <td>{{book.title}}</td>
            <td>{{book.author}}</td>
            <td>
              <span v-if="book.read">Yes</span>
              <span v-else>No</span>
            </td>
            <td>
              <button
                type="button"
                class="btn btn-warning btn-sm"
                v-b-modal.book-update-modal
                @click="editBook(book)">
                Update
              </button>
              <button
                type="button"
                class="btn btn-danger btn-sm"
                @click="onDeleteBook(book)">
                Delete
              </button>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>

    <b-modal ref="addBookModal"
             id="book-modal"
             title="Add a new book"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-title-group"
                      label="Title:"
                      label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addBookForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
                      label="Author:"
                      label-for="form-author-input">
          <b-form-input id="form-author-input"
                        type="text"
                        v-model="addBookForm.author"
                        required
                        placeholder="Enter author">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-read-group">
          <b-form-checkbox-group v-model="addBookForm.read" id="form-checks">
            <b-form-checkbox value="true">Read?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>

    <b-modal ref="editBookModal"
             id="book-update-modal"
             title="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-title-edit-group"
                      label="Title:"
                      label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="editForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-edit-group"
                      label="Author:"
                      label-for="form-author-edit-input">
          <b-form-input id="form-author-edit-input"
                        type="text"
                        v-model="editForm.author"
                        required
                        placeholder="Enter author">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-read-edit-group">
          <b-form-checkbox-group v-model="editForm.read" id="form-checks">
            <b-form-checkbox value="true">Read?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button type="submit" variant="primary">Update</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>

  </div>
</template>

<script>
  import axios from 'axios'
  import Alert from './Alert'
  const booksUrl = 'http://localhost:5000/books'

  export default {
    data() {
      return {
        books: [],
        addBookForm: {
          title: '',
          author: '',
          read: false,
        },
        editForm: {
          id: '',
          title: '',
          author: '',
          read: false,
        },
      }
    },
    components: {
      alert: Alert,
    },
    methods: {
      getBooks() {
        axios.get(booksUrl)
          .then((res) => {
            let books = []
            for (let key in res.data.books) {
              let book = res.data.books[key]
              book.id = key
              books.push(book)
            }
            this.books = books
          })
          .catch((error) => {
            console.log('Ohhh snaaap')
            console.error(error)
          })
      },
      addBook(payload) {
        axios.post(booksUrl, payload)
          .then(() => {
            this.$refs.alert.showSuccess(`Book '${payload['title']}' added!`)
            this.getBooks()
          })
          .catch((error) => {
            let msg = error.response.data.message
            this.$refs.alert.showError(msg)
            console.log(error)
            this.getBooks()
          })
      },
      editBook(book) {
        this.editForm = book
      },
      initForm() {
        this.addBookForm.title = ''
        this.addBookForm.author = ''
        this.addBookForm.read = false
        this.editForm.id = ''
        this.editForm.title = ''
        this.editForm.author = ''
        this.editForm.read = false
      },
      onSubmit(evt) {
        evt.preventDefault()
        this.$refs.addBookModal.hide()
        let read = false
        if (this.addBookForm.read[0]) read = true
        const payload = {
          title: this.addBookForm.title,
          author: this.addBookForm.author,
          read,
        }
        this.addBook(payload)
        this.initForm()
      },
      onReset(evt) {
        evt.preventDefault()
        this.$refs.addBookModal.hide()
        this.initForm()
      },
      onSubmitUpdate(evt) {
        evt.preventDefault()
        this.$refs.editBookModal.hide()
        const payload = {
          title: this.editForm.title,
          author: this.editForm.author,
          read: this.editForm.read,
        }
        this.updateBook(payload, this.editForm.id)
      },
      updateBook(payload, bookID) {
        axios.put(booksUrl + bookID, payload)
          .then(() => {
            this.$refs.alert.showSuccess('Book successfully updated.')
            this.getBooks()
          })
          .catch((error) => {
            let msg = error.response.data.message
            this.$refs.alert.showError(msg)
            this.getBooks()
          })
      },
      onResetUpdate(evt) {
        evt.preventDefault()
        this.$refs.editBookModal.hide()
        this.initForm()
        this.getBooks() // todo: why?
      },
      removeBook(bookID) {
        axios.delete(booksUrl + bookID)
          .then(() => {
            this.getBooks()
            this.$refs.alert.showSuccess('Book removed!')
          })
          .catch((error) => {
            let msg = error.response.data.message
            this.$refs.alert.showError(msg)
            console.error(error)
            this.getBooks()
          })
      },
      onDeleteBook(book) {
        this.removeBook(book.id)
      },
    },
    created() {
      this.getBooks()
    },
  }
</script>

<style scoped>

</style>
